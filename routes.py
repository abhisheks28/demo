from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models import User, Product, Category, Order, OrderItem, Cart, Wishlist, Payment
from utils import admin_required, super_admin_required, generate_unique_code, allowed_file
import os
from datetime import datetime, timedelta
from sqlalchemy import func, desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get featured products (latest 8 products)
    featured_products = Product.query.filter_by(is_active=True).order_by(desc(Product.created_at)).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', featured_products=featured_products, categories=categories)

# Admin Routes
@main_bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Analytics data
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    total_users = User.query.filter_by(role='customer').count()
    total_super_admins = User.query.filter_by(role='super_admin').count()
    
    # Monthly revenue for last 6 months
    monthly_revenue = []
    for i in range(6):
        start_date = datetime.now().replace(day=1) - timedelta(days=30*i)
        end_date = (start_date + timedelta(days=32)).replace(day=1)
        revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= start_date,
            Order.created_at < end_date
        ).scalar() or 0
        monthly_revenue.append({
            'month': start_date.strftime('%B %Y'),
            'revenue': float(revenue)
        })
    
    # Order status breakdown
    status_counts = db.session.query(
        Order.status, func.count(Order.id)
    ).group_by(Order.status).all()
    
    # Top selling products
    top_products = db.session.query(
        Product.name, func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.id).order_by(desc('total_sold')).limit(5).all()
    
    # Recent orders
    recent_orders = Order.query.order_by(desc(Order.created_at)).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_users=total_users,
                         total_super_admins=total_super_admins,
                         monthly_revenue=monthly_revenue,
                         status_counts=status_counts,
                         top_products=top_products,
                         recent_orders=recent_orders)

@main_bp.route('/admin/super-admins')
@login_required
@admin_required
def admin_super_admins():
    super_admins = User.query.filter_by(role='super_admin').all()
    return render_template('admin/super_admins.html', super_admins=super_admins)

@main_bp.route('/admin/create-super-admin', methods=['POST'])
@login_required
@admin_required
def create_super_admin():
    username = request.form.get('username')
    email = request.form.get('email')
    category_name = request.form.get('category')
    
    if not all([username, email, category_name]):
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('main.admin_super_admins'))
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        flash('Email already exists.', 'error')
        return redirect(url_for('main.admin_super_admins'))
    
    # Generate unique code
    unique_code = generate_unique_code()
    
    # Create or get category
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name, description=f'Products for {category_name}')
        db.session.add(category)
    
    # Create admin user with unique code (they will register later)
    admin_user = User(
        name=username,
        email=email,
        password_hash='',  # Will be set during registration
        role='admin',
        unique_code=unique_code,
        is_active=False  # Will be activated after registration
    )
    
    try:
        db.session.add(admin_user)
        db.session.commit()
        flash(f'Super Admin created successfully! Unique code: {unique_code}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to create Super Admin.', 'error')
    
    return redirect(url_for('main.admin_super_admins'))

@main_bp.route('/admin/toggle-super-admin/<int:user_id>')
@login_required
@admin_required
def toggle_super_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'super_admin':
        user.is_active = not user.is_active
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'Super Admin {status} successfully.', 'success')
    return redirect(url_for('main.admin_super_admins'))

# Super Admin Routes
@main_bp.route('/super-admin/dashboard')
@login_required
@super_admin_required
def super_admin_dashboard():
    # Get super admin's products and stats
    products_count = Product.query.filter_by(super_admin_id=current_user.id).count()
    
    # Orders for super admin's products
    orders_count = db.session.query(Order).join(OrderItem).join(Product).filter(
        Product.super_admin_id == current_user.id
    ).count()
    
    # Revenue from super admin's products
    revenue = db.session.query(func.sum(OrderItem.price * OrderItem.quantity)).join(Product).filter(
        Product.super_admin_id == current_user.id
    ).scalar() or 0
    
    # Low stock products (less than 10)
    low_stock_products = Product.query.filter_by(
        super_admin_id=current_user.id
    ).filter(Product.stock < 10).all()
    
    # Recent orders for super admin's products
    recent_orders = db.session.query(Order).join(OrderItem).join(Product).filter(
        Product.super_admin_id == current_user.id
    ).order_by(desc(Order.created_at)).limit(10).all()
    
    return render_template('super_admin/dashboard.html',
                         products_count=products_count,
                         orders_count=orders_count,
                         revenue=revenue,
                         low_stock_products=low_stock_products,
                         recent_orders=recent_orders)

@main_bp.route('/super-admin/products')
@login_required
@super_admin_required
def super_admin_products():
    products = Product.query.filter_by(super_admin_id=current_user.id).all()
    return render_template('super_admin/products.html', products=products)

@main_bp.route('/super-admin/add-product', methods=['GET', 'POST'])
@login_required
@super_admin_required
def add_product():
    categories = Category.query.all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        
        if not all([name, price, stock, category_id]):
            flash('Please fill in all required fields.', 'error')
            return render_template('super_admin/add_product.html', categories=categories)
        
        try:
            product = Product(
                name=name,
                description=description,
                price=float(price),
                stock=int(stock),
                category_id=int(category_id),
                super_admin_id=current_user.id
            )
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to filename to avoid conflicts
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    product.image_url = f"/static/uploads/{filename}"
            
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('main.super_admin_products'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to add product.', 'error')
    
    return render_template('super_admin/add_product.html', categories=categories)

@main_bp.route('/super-admin/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@super_admin_required
def edit_product(product_id):
    product = Product.query.filter_by(id=product_id, super_admin_id=current_user.id).first_or_404()
    categories = Category.query.all()
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id'))
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product.image_url = f"/static/uploads/{filename}"
        
        try:
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('main.super_admin_products'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update product.', 'error')
    
    return render_template('super_admin/edit_product.html', product=product, categories=categories)

@main_bp.route('/super-admin/delete-product/<int:product_id>')
@login_required
@super_admin_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, super_admin_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete product.', 'error')
    
    return redirect(url_for('main.super_admin_products'))

@main_bp.route('/super-admin/orders')
@login_required
@super_admin_required
def super_admin_orders():
    # Get orders containing super admin's products
    orders = db.session.query(Order).join(OrderItem).join(Product).filter(
        Product.super_admin_id == current_user.id
    ).distinct().order_by(desc(Order.created_at)).all()
    
    return render_template('super_admin/orders.html', orders=orders)

@main_bp.route('/super-admin/update-order-status/<int:order_id>')
@login_required
@super_admin_required
def update_order_status(order_id):
    status = request.args.get('status')
    order = Order.query.get_or_404(order_id)
    
    if status in ['processing', 'shipped', 'delivered']:
        order.status = status
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    else:
        flash('Invalid status.', 'error')
    
    return redirect(url_for('main.super_admin_orders'))

# Customer Routes
@main_bp.route('/products')
def products():
    category_id = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.all()
    categories = Category.query.all()
    
    return render_template('customer/products.html', products=products, categories=categories)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    return render_template('customer/product_detail.html', product=product)

@main_bp.route('/add-to-cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    # Check if item already in cart
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('main.product_detail', product_id=product_id))

@main_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('customer/cart.html', cart_items=cart_items, total=total)

@main_bp.route('/update-cart/<int:cart_id>')
@login_required
def update_cart(cart_id):
    action = request.args.get('action')
    cart_item = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first_or_404()
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
    elif action == 'remove':
        db.session.delete(cart_item)
    
    db.session.commit()
    return redirect(url_for('main.cart'))

@main_bp.route('/add-to-wishlist/<int:product_id>')
@login_required
def add_to_wishlist(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if not existing:
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Product added to wishlist!', 'success')
    else:
        flash('Product already in wishlist!', 'info')
    
    return redirect(url_for('main.product_detail', product_id=product_id))

@main_bp.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('customer/wishlist.html', wishlist_items=wishlist_items)

@main_bp.route('/remove-from-wishlist/<int:wishlist_id>')
@login_required
def remove_from_wishlist(wishlist_id):
    wishlist_item = Wishlist.query.filter_by(id=wishlist_id, user_id=current_user.id).first_or_404()
    db.session.delete(wishlist_item)
    db.session.commit()
    flash('Product removed from wishlist!', 'success')
    return redirect(url_for('main.wishlist'))

@main_bp.route('/checkout')
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('main.cart'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('customer/checkout.html', cart_items=cart_items, total=total)

@main_bp.route('/place-order', methods=['POST'])
@login_required
def place_order():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('main.cart'))
    
    address = request.form.get('address')
    phone = request.form.get('phone')
    payment_method = request.form.get('payment_method')
    
    if not all([address, phone, payment_method]):
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('main.checkout'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create order
    order = Order(
        customer_id=current_user.id,
        total_amount=total,
        payment_method=payment_method,
        shipping_address=address,
        phone=phone
    )
    
    if payment_method == 'online':
        order.payment_status = 'paid'  # Simulate successful payment
    
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
        
        # Update product stock
        cart_item.product.stock -= cart_item.quantity
    
    # Create payment record
    payment = Payment(
        order_id=order.id,
        payment_method=payment_method,
        payment_status='paid' if payment_method == 'online' else 'pending',
        amount=total,
        transaction_id=f"TXN{order.id}{datetime.now().strftime('%Y%m%d%H%M%S')}" if payment_method == 'online' else None
    )
    db.session.add(payment)
    
    # Clear cart
    Cart.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('main.orders'))

@main_bp.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(customer_id=current_user.id).order_by(desc(Order.created_at)).all()
    return render_template('customer/orders.html', orders=user_orders)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('customer/profile.html')

@main_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if not all([name, email]):
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('main.profile'))
    
    # Check if email is taken by another user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Email already taken by another user.', 'error')
        return redirect(url_for('main.profile'))
    
    current_user.name = name
    current_user.email = email
    
    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update profile.', 'error')
    
    return redirect(url_for('main.profile'))
