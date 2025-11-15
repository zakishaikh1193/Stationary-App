const API_URL = 'https://stationary-app-production.up.railway.app/api';
const USER_ID = 1; // Demo user

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadOrders();
    updateCartBadge();
    
    // Modal controls
    const modal = document.getElementById('orderDetailModal');
    const closeBtn = modal.querySelector('.close');
    closeBtn.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target == modal) modal.style.display = 'none';
    });
});

// Load orders
async function loadOrders() {
    const loading = document.getElementById('loading');
    const ordersList = document.getElementById('ordersList');
    const emptyState = document.getElementById('emptyState');
    
    try {
        loading.style.display = 'block';
        
        const response = await fetch(`${API_URL}/orders/${USER_ID}`);
        const data = await response.json();
        
        if (response.ok) {
            const orders = data.orders || [];
            
            if (orders.length > 0) {
                displayOrders(orders);
                ordersList.style.display = 'flex';
                emptyState.style.display = 'none';
            } else {
                ordersList.style.display = 'none';
                emptyState.style.display = 'flex';
            }
        } else {
            showToast(data.error || 'Failed to load orders', 'error');
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        showToast('Failed to load orders. Please try again.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display orders
function displayOrders(orders) {
    const ordersList = document.getElementById('ordersList');
    
    ordersList.innerHTML = orders.map(order => {
        const date = new Date(order.created_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        return `
            <div class="order-card">
                <div class="order-header">
                    <div>
                        <div class="order-number">Order #${order.id}</div>
                        <div class="order-date">${date}</div>
                    </div>
                    <span class="order-status ${order.status}">${capitalizeFirst(order.status)}</span>
                </div>
                
                <div class="order-footer">
                    <div class="order-total">
                        <div class="order-total-row">
                            <span>Subtotal:</span>
                            <span>$${parseFloat(order.total_amount).toFixed(2)}</span>
                        </div>
                        <div class="order-total-row">
                            <span>Tax:</span>
                            <span>$${parseFloat(order.tax_amount).toFixed(2)}</span>
                        </div>
                        <div class="order-total-row grand">
                            <span>Grand Total:</span>
                            <span>$${parseFloat(order.grand_total).toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="order-actions">
                        <button onclick="viewOrderDetails(${order.id})" class="btn btn-primary">
                            <i class="fas fa-eye"></i> View Details
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// View order details
async function viewOrderDetails(orderId) {
    try {
        const response = await fetch(`${API_URL}/orders/detail/${orderId}`);
        const data = await response.json();
        
        if (response.ok) {
            showOrderDetailModal(data.order);
        } else {
            showToast(data.error || 'Failed to load order details', 'error');
        }
    } catch (error) {
        console.error('Error loading order details:', error);
        showToast('Failed to load order details. Please try again.', 'error');
    }
}

// Show order detail modal
function showOrderDetailModal(order) {
    const modal = document.getElementById('orderDetailModal');
    const modalBody = document.getElementById('orderDetailBody');
    
    const date = new Date(order.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    modalBody.innerHTML = `
        <div class="order-detail-modal">
            <div class="order-detail-header">
                <h2>Order #${order.id}</h2>
                <span class="order-status ${order.status}">${capitalizeFirst(order.status)}</span>
            </div>
            <div class="order-detail-date">${date}</div>
            
            <div class="order-items-section">
                <h3>Order Items</h3>
                <div class="order-items-list">
                    ${order.items.map(item => {
                        const imageUrl = item.image_url || 'https://via.placeholder.com/80x80?text=Product';
                        return `
                            <div class="order-item-row">
                                <div class="order-item-image">
                                    <img src="${imageUrl}" alt="${item.product_name}"
                                         onerror="this.src='https://via.placeholder.com/80x80?text=No+Image'">
                                </div>
                                <div class="order-item-details">
                                    <h4>${item.product_name}</h4>
                                    <div class="item-meta">Price: $${parseFloat(item.product_price).toFixed(2)}</div>
                                </div>
                                <div class="order-item-quantity">
                                    Qty: ${item.quantity}
                                </div>
                                <div class="order-item-price">
                                    $${parseFloat(item.subtotal).toFixed(2)}
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
            
            <div class="order-summary-section">
                <div class="order-total">
                    <div class="order-total-row">
                        <span>Subtotal:</span>
                        <span>$${parseFloat(order.total_amount).toFixed(2)}</span>
                    </div>
                    <div class="order-total-row">
                        <span>Tax (10%):</span>
                        <span>$${parseFloat(order.tax_amount).toFixed(2)}</span>
                    </div>
                    <div class="order-total-row grand">
                        <span>Grand Total:</span>
                        <span>$${parseFloat(order.grand_total).toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Update cart badge
async function updateCartBadge() {
    try {
        const response = await fetch(`${API_URL}/cart/${USER_ID}`);
        const data = await response.json();
        
        if (response.ok) {
            const badge = document.getElementById('cartBadge');
            const itemCount = data.item_count || 0;
            badge.textContent = itemCount;
            badge.style.display = itemCount > 0 ? 'inline-block' : 'none';
        }
    } catch (error) {
        console.error('Error updating cart badge:', error);
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Capitalize first letter
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

