// MSR Shop - Charts and Analytics

// Chart.js Global Configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#6c757d';

// Initialize Charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeAdminCharts();
    initializeSuperAdminCharts();
});

// Admin Dashboard Charts
function initializeAdminCharts() {
    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart');
    if (revenueCtx && typeof revenueData !== 'undefined') {
        createRevenueChart(revenueCtx, revenueData);
    }
    
    // Order Status Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx && typeof statusData !== 'undefined') {
        createStatusChart(statusCtx, statusData);
    }
    
    // Sales Trend Chart
    const salesTrendCtx = document.getElementById('salesTrendChart');
    if (salesTrendCtx && typeof salesTrendData !== 'undefined') {
        createSalesTrendChart(salesTrendCtx, salesTrendData);
    }
    
    // Top Products Chart
    const topProductsCtx = document.getElementById('topProductsChart');
    if (topProductsCtx && typeof topProductsData !== 'undefined') {
        createTopProductsChart(topProductsCtx, topProductsData);
    }
}

// Revenue Line Chart
function createRevenueChart(ctx, data) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.month),
            datasets: [{
                label: 'Revenue ($)',
                data: data.map(item => item.revenue),
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#0d6efd',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Monthly Revenue Trend',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            elements: {
                point: {
                    hoverBackgroundColor: '#0d6efd'
                }
            }
        }
    });
}

// Order Status Doughnut Chart
function createStatusChart(ctx, data) {
    const colors = {
        'pending': '#ffc107',
        'processing': '#0d6efd',
        'shipped': '#0dcaf0',
        'delivered': '#198754',
        'cancelled': '#dc3545'
    };
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item[0].charAt(0).toUpperCase() + item[0].slice(1)),
            datasets: [{
                data: data.map(item => item[1]),
                backgroundColor: data.map(item => colors[item[0]] || '#6c757d'),
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 11
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Order Status Distribution',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            },
            cutout: '60%',
            elements: {
                arc: {
                    hoverOffset: 10
                }
            }
        }
    });
}

// Sales Trend Area Chart
function createSalesTrendChart(ctx, data) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Sales',
                data: data.sales,
                borderColor: '#198754',
                backgroundColor: 'rgba(25, 135, 84, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }, {
                label: 'Orders',
                data: data.orders,
                borderColor: '#0dcaf0',
                backgroundColor: 'rgba(13, 202, 240, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    align: 'end'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Top Products Bar Chart
function createTopProductsChart(ctx, data) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item[0].length > 20 ? item[0].substring(0, 20) + '...' : item[0]),
            datasets: [{
                label: 'Units Sold',
                data: data.map(item => item[1]),
                backgroundColor: 'rgba(13, 110, 253, 0.8)',
                borderColor: '#0d6efd',
                borderWidth: 1,
                borderRadius: 4,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top Selling Products',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            elements: {
                bar: {
                    hoverBackgroundColor: '#0051d2'
                }
            }
        }
    });
}

// Super Admin Dashboard Charts
function initializeSuperAdminCharts() {
    // Stock Levels Chart
    const stockCtx = document.getElementById('stockChart');
    if (stockCtx && typeof stockData !== 'undefined') {
        createStockChart(stockCtx, stockData);
    }
    
    // Sales Performance Chart
    const performanceCtx = document.getElementById('performanceChart');
    if (performanceCtx && typeof performanceData !== 'undefined') {
        createPerformanceChart(performanceCtx, performanceData);
    }
}

// Stock Levels Bar Chart
function createStockChart(ctx, data) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.name),
            datasets: [{
                label: 'Stock Level',
                data: data.map(item => item.stock),
                backgroundColor: data.map(item => {
                    if (item.stock === 0) return '#dc3545';
                    if (item.stock < 10) return '#ffc107';
                    if (item.stock < 50) return '#fd7e14';
                    return '#198754';
                }),
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Product Stock Levels',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45
                    }
                }
            }
        }
    });
}

// Performance Line Chart
function createPerformanceChart(ctx, data) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Revenue',
                data: data.revenue,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                yAxisID: 'y'
            }, {
                label: 'Orders',
                data: data.orders,
                borderColor: '#198754',
                backgroundColor: 'rgba(25, 135, 84, 0.1)',
                borderWidth: 2,
                fill: false,
                tension: 0.4,
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Utility function to create simple metric charts
function createMetricChart(canvasId, value, max, color, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const percentage = (value / max) * 100;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, max - value],
                backgroundColor: [color, 'rgba(0, 0, 0, 0.1)'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            elements: {
                arc: {
                    borderWidth: 0
                }
            }
        },
        plugins: [{
            beforeDraw: function(chart) {
                const width = chart.width;
                const height = chart.height;
                const ctx = chart.ctx;
                
                ctx.restore();
                const fontSize = (height / 100).toFixed(2);
                ctx.font = fontSize + "em Arial";
                ctx.textBaseline = "middle";
                ctx.fillStyle = color;
                
                const text = Math.round(percentage) + "%";
                const textX = Math.round((width - ctx.measureText(text).width) / 2);
                const textY = height / 2;
                
                ctx.fillText(text, textX, textY);
                ctx.save();
            }
        }]
    });
}

// Real-time Updates (for future enhancement)
function updateChartData(chart, newData) {
    chart.data.datasets[0].data = newData;
    chart.update('none');
}

// Export Chart as Image
function exportChart(chartInstance, filename) {
    const link = document.createElement('a');
    link.download = filename || 'chart.png';
    link.href = chartInstance.toBase64Image();
    link.click();
}

// Responsive Chart Handling
function handleChartResize() {
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.resize();
    });
}

// Listen for window resize
window.addEventListener('resize', function() {
    setTimeout(handleChartResize, 300);
});

// Chart Animation Options
const animationOptions = {
    tension: {
        duration: 1000,
        easing: 'easeOutBounce',
        from: 1,
        to: 0,
        loop: false
    }
};

// Color Schemes
const colorSchemes = {
    primary: ['#0d6efd', '#6610f2', '#6f42c1', '#d63384', '#dc3545'],
    success: ['#198754', '#20c997', '#0dcaf0', '#6610f2', '#6f42c1'],
    warning: ['#ffc107', '#fd7e14', '#dc3545', '#d63384', '#6f42c1'],
    gradient: {
        blue: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        green: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        orange: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    }
};

// Chart Themes
function applyLightTheme(chart) {
    chart.options.plugins.legend.labels.color = '#6c757d';
    chart.options.scales.x.ticks.color = '#6c757d';
    chart.options.scales.y.ticks.color = '#6c757d';
    chart.options.scales.x.grid.color = 'rgba(0, 0, 0, 0.05)';
    chart.options.scales.y.grid.color = 'rgba(0, 0, 0, 0.05)';
    chart.update();
}

// Initialize chart themes
document.addEventListener('DOMContentLoaded', function() {
    // Apply light theme to all charts
    setTimeout(() => {
        Chart.helpers.each(Chart.instances, function(instance) {
            applyLightTheme(instance);
        });
    }, 1000);
});
