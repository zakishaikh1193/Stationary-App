const API_URL = 'http://127.0.0.1:5000/api';
const USER_ID = 1; // Demo user

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadCart();
    document.getElementById('checkoutBtn').addEventListener('click', checkout);
});

// Load cart items
async function loadCart() {
    const loading = document.getElementById('loading');
    const cartItems = document.getElementById('cartItems');
    const emptyCart = document.getElementById('emptyCart');
    const cartContent = document.querySelector('.cart-content');
    
    try {
        loading.style.display = 'block';
        
        const response = await fetch(`${API_URL}/cart/${USER_ID}`);
        const data = await response.json();
        
        if (response.ok) {
            if (data.cart_items && data.cart_items.length > 0) {
                displayCartItems(data.cart_items);
                updateSummary(data);
                cartContent.style.display = 'grid';
                emptyCart.style.display = 'none';
            } else {
                cartContent.style.display = 'none';
                emptyCart.style.display = 'flex';
            }
            updateCartBadge(data.item_count);
        } else {
            showToast(data.error || 'Failed to load cart', 'error');
        }
    } catch (error) {
        console.error('Error loading cart:', error);
        showToast('Failed to load cart. Please try again.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display cart items
function displayCartItems(items) {
    const cartItems = document.getElementById('cartItems');
    
    cartItems.innerHTML = items.map(item => {
        const imageUrl = item.image_url || 'https://via.placeholder.com/150x150?text=Product';
        const subtotal = parseFloat(item.subtotal).toFixed(2);
        const price = parseFloat(item.price).toFixed(2);
        
        return `
            <div class="cart-item" data-cart-id="${item.id}">
                <div class="cart-item-image">
                    <img src="${imageUrl}" alt="${item.name}" 
                         onerror="this.src='https://via.placeholder.com/150x150?text=No+Image'">
                </div>
                <div class="cart-item-details">
                    <h3>${item.name}</h3>
                    <p class="item-description">${truncateText(item.description, 100)}</p>
                    <div class="item-price">$${price}</div>
                </div>
                <div class="cart-item-quantity">
                    <label>Quantity:</label>
                    <div class="quantity-controls">
                        <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})" class="qty-btn">
                            <i class="fas fa-minus"></i>
                        </button>
                        <input type="number" value="${item.quantity}" min="1" max="${item.stock}" 
                               onchange="updateQuantity(${item.id}, this.value)" 
                               class="qty-input">
                        <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})" 
                                class="qty-btn" ${item.quantity >= item.stock ? 'disabled' : ''}>
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    <div class="stock-info">Max: ${item.stock}</div>
                </div>
                <div class="cart-item-subtotal">
                    <div class="subtotal-label">Subtotal:</div>
                    <div class="subtotal-amount">$${subtotal}</div>
                </div>
                <div class="cart-item-remove">
                    <button onclick="removeItem(${item.id})" class="btn-icon btn-delete" title="Remove">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Update cart summary
function updateSummary(data) {
    const subtotal = parseFloat(data.total || 0);
    const tax = subtotal * 0.1;
    const total = subtotal + tax;
    
    document.getElementById('itemCount').textContent = data.item_count || 0;
    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

// Update quantity
async function updateQuantity(cartItemId, newQuantity) {
    newQuantity = parseInt(newQuantity);
    
    if (newQuantity < 0) {
        return;
    }
    
    if (newQuantity === 0) {
        removeItem(cartItemId);
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/cart/${cartItemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity: newQuantity })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            loadCart(); // Reload cart
        } else {
            showToast(data.error || 'Failed to update quantity', 'error');
        }
    } catch (error) {
        console.error('Error updating quantity:', error);
        showToast('Failed to update quantity. Please try again.', 'error');
    }
}

// Remove item
async function removeItem(cartItemId) {
    if (!confirm('Remove this item from cart?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/cart/${cartItemId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Item removed from cart', 'success');
            loadCart(); // Reload cart
        } else {
            showToast(data.error || 'Failed to remove item', 'error');
        }
    } catch (error) {
        console.error('Error removing item:', error);
        showToast('Failed to remove item. Please try again.', 'error');
    }
}

// Checkout
async function checkout() {
    try {
        const response = await fetch(`${API_URL}/cart/${USER_ID}`);
        const data = await response.json();
        
        if (response.ok && data.cart_items && data.cart_items.length > 0) {
            // Process checkout
            const checkoutResponse = await fetch(`${API_URL}/orders/checkout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: USER_ID })
            });
            
            const checkoutData = await checkoutResponse.json();
            
            if (checkoutResponse.ok) {
                // Show success popup
                showSuccessPopup(checkoutData.order_id, checkoutData.grand_total);
                
                // Reload cart after a delay
                setTimeout(() => {
                    loadCart();
                }, 2000);
            } else {
                showToast(checkoutData.error || 'Checkout failed', 'error');
            }
        } else {
            showToast('Your cart is empty!', 'error');
        }
    } catch (error) {
        console.error('Error during checkout:', error);
        showToast('Checkout failed. Please try again.', 'error');
    }
}

// Show success popup
function showSuccessPopup(orderId, total) {
    // Create popup backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'popup-backdrop';
    backdrop.style.display = 'block';
    
    // Create popup
    const popup = document.createElement('div');
    popup.className = 'success-popup';
    popup.innerHTML = `
        <div class="success-icon">
            <i class="fas fa-check-circle"></i>
        </div>
        <h2>Order Placed Successfully! 🎉</h2>
        <p>Your order has been confirmed and is being processed.</p>
        <div class="order-summary-popup">
            <div class="summary-item">
                <span>Order Number:</span>
                <strong>#${orderId}</strong>
            </div>
            <div class="summary-item">
                <span>Total Amount:</span>
                <strong class="total-highlight">$${parseFloat(total).toFixed(2)}</strong>
            </div>
        </div>
        <div class="popup-actions">
            <a href="orders.html" class="btn btn-primary">
                <i class="fas fa-list"></i> View My Orders
            </a>
            <a href="shop.html" class="btn btn-secondary">
                <i class="fas fa-shopping-bag"></i> Continue Shopping
            </a>
        </div>
        <button class="close-popup">&times;</button>
    `;
    
    // Add to body
    document.body.appendChild(backdrop);
    document.body.appendChild(popup);
    
    // Animate in
    setTimeout(() => {
        backdrop.classList.add('show');
        popup.classList.add('show');
    }, 10);
    
    // Close handlers
    const closePopup = () => {
        backdrop.classList.remove('show');
        popup.classList.remove('show');
        setTimeout(() => {
            backdrop.remove();
            popup.remove();
        }, 300);
    };
    
    popup.querySelector('.close-popup').addEventListener('click', closePopup);
    backdrop.addEventListener('click', closePopup);
}

// Update cart badge
function updateCartBadge(count) {
    const badge = document.getElementById('cartBadge');
    badge.textContent = count || 0;
    badge.style.display = count > 0 ? 'inline-block' : 'none';
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

// Truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

