# MSR Shop - E-Commerce Platform

## Overview

MSR Shop is a multi-role e-commerce platform built with Flask, designed to support three distinct user roles: Admin, Super Admin, and Customer. The platform provides a comprehensive marketplace solution where Super Admins can manage their own products, Admins oversee the entire platform with analytics and reports, and Customers can browse, purchase, and manage their orders. The application features a clean, Bootstrap-based interface with real-time analytics, secure authentication, and role-based access control.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python micro-framework) with modular blueprint structure
- **Database ORM**: SQLAlchemy with declarative base model for database operations
- **Authentication**: Flask-Login for session management with role-based access control
- **File Handling**: Werkzeug utilities for secure file uploads with configurable size limits
- **Application Factory Pattern**: Centralized app creation with extension initialization

### Frontend Architecture
- **Template Engine**: Jinja2 templating with template inheritance
- **CSS Framework**: Bootstrap 5 for responsive design and components
- **JavaScript**: Vanilla JS with Chart.js for analytics visualization
- **Icon Library**: Font Awesome for consistent iconography
- **Static Asset Management**: Flask's static file serving with organized CSS/JS structure

### Database Design
- **User Management**: Role-based user system (admin, super_admin, customer) with secure password hashing
- **Product Catalog**: Hierarchical product-category relationship with image support
- **Order Management**: Complete order lifecycle with status tracking and payment methods
- **Shopping Features**: Shopping cart and wishlist functionality with user associations
- **Analytics Support**: Database structure optimized for reporting and dashboard metrics

### Authentication & Authorization
- **Session-Based Authentication**: Flask-Login with secure session management
- **Role-Based Access Control**: Decorator-based route protection for different user roles
- **Password Security**: Werkzeug password hashing with secure random code generation
- **Unique Code System**: Special registration codes for Super Admin role assignment

### File Upload System
- **Secure File Handling**: Werkzeug secure filename processing with extension validation
- **Image Management**: Product image upload with configurable storage paths
- **File Size Limits**: 16MB maximum file upload limit with proper error handling
- **Storage Organization**: Structured static file organization for uploads

### Error Handling & Logging
- **Comprehensive Logging**: Debug-level logging configuration for development
- **Flash Message System**: User-friendly error and success message display
- **Form Validation**: Both client-side and server-side validation
- **Graceful Error Recovery**: Proper error handling with user feedback

## External Dependencies

### Core Framework Dependencies
- **Flask**: Primary web framework with SQLAlchemy integration
- **Flask-SQLAlchemy**: Database ORM for model management and queries
- **Flask-Login**: User session management and authentication
- **Werkzeug**: WSGI utilities for security and file handling

### Frontend Libraries
- **Bootstrap 5**: CSS framework via CDN for responsive design
- **Font Awesome 6**: Icon library via CDN for UI elements
- **Chart.js**: JavaScript charting library via CDN for analytics visualization

### Database Infrastructure
- **SQLAlchemy**: Database abstraction layer with PostgreSQL support expected
- **Database Connection**: Environment-based configuration with connection pooling
- **Migration Support**: Database schema management capabilities

### Development & Deployment
- **ProxyFix Middleware**: Werkzeug proxy handling for deployment environments
- **Environment Configuration**: Environment variable-based configuration for secrets
- **Static File Serving**: Flask's built-in static file handling for development

### Payment Integration (Planned)
- **Payment Gateways**: Architecture prepared for Razorpay/Stripe integration
- **Cash on Delivery**: Alternative payment method support
- **Payment Status Tracking**: Database structure for payment management