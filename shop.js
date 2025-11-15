const API_URL = 'http://127.0.0.1:5000/api';
let allProducts = [];
let currentUser = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    updateCartBadge();
    
    // Event listeners
    document.getElementById('searchInput').addEventListener('input', filterProducts);
    document.getElementById('categoryFilter').addEventListener('change', filterProducts);
    
    // Modal close
    const modal = document.getElementById('productModal');
    const closeBtn = modal.querySelector('.close');
    closeBtn.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => {
        if (e.target == modal) modal.style.display = 'none';
    };
});

// Load products from API
async function loadProducts() {
    const loading = document.getElementById('loading');
    const productsGrid = document.getElementById('productsGrid');
    const errorMessage = document.getElementById('errorMessage');
    
    try {
        loading.style.display = 'block';
        errorMessage.style.display = 'none';
        
        const response = await fetch(`${API_URL}/products`);
        const data = await response.json();
        
        if (response.ok) {
            allProducts = data.products || [];
            displayProducts(allProducts);
        } else {
            throw new Error(data.error || 'Failed to load products');
        }
    } catch (error) {
        console.error('Error loading products:', error);
        errorMessage.textContent = 'Failed to load products. Please try again later.';
        errorMessage.style.display = 'block';
        productsGrid.innerHTML = '';
    } finally {
        loading.style.display = 'none';
    }
}

// Display products
function displayProducts(products) {
    const productsGrid = document.getElementById('productsGrid');
    const emptyState = document.getElementById('emptyState');
    
    if (products.length === 0) {
        productsGrid.innerHTML = '';
        emptyState.style.display = 'flex';
        return;
    }
    
    emptyState.style.display = 'none';
    productsGrid.innerHTML = products.map(product => createProductCard(product)).join('');
    
    // Add event listeners to buttons
    products.forEach(product => {
        document.getElementById(`add-${product.id}`).addEventListener('click', () => addToCart(product));
        document.getElementById(`view-${product.id}`).addEventListener('click', () => viewProduct(product));
    });
}

// Create product card HTML
function createProductCard(product) {
    const imageUrl = product.image_url || 'https://via.placeholder.com/300x200?text=Product+Image';
    const stockStatus = product.stock > 0 ? 'in-stock' : 'out-of-stock';
    const stockText = product.stock > 0 ? `${product.stock} in stock` : 'Out of stock';
    
    return `
        <div class="product-card" data-category="${product.category}">
            <div class="product-image">
                <img src="${imageUrl}" alt="${product.name}" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                ${product.stock === 0 ? '<div class="out-of-stock-overlay">Out of Stock</div>' : ''}
            </div>
            <div class="product-info">
                <div class="product-category">${product.category || 'Uncategorized'}</div>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${truncateText(product.description, 80)}</p>
                <div class="product-footer">
                    <div class="product-price">$${parseFloat(product.price).toFixed(2)}</div>
                    <div class="product-stock ${stockStatus}">${stockText}</div>
                </div>
                <div class="product-actions">
                    <button id="view-${product.id}" class="btn btn-secondary">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button id="add-${product.id}" class="btn btn-primary" ${product.stock === 0 ? 'disabled' : ''}>
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Filter products
function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;
    
    const filtered = allProducts.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) ||
                            (product.description && product.description.toLowerCase().includes(searchTerm));
        const matchesCategory = !category || product.category === category;
        return matchesSearch && matchesCategory;
    });
    
    displayProducts(filtered);
}

// View product details
function viewProduct(product) {
    const modal = document.getElementById('productModal');
    const modalBody = document.getElementById('modalBody');
    const imageUrl = product.image_url || 'https://via.placeholder.com/400x300?text=Product+Image';
    
    modalBody.innerHTML = `
        <div class="product-detail">
            <div class="product-detail-image">
                <img src="${imageUrl}" alt="${product.name}" onerror="this.src='https://via.placeholder.com/400x300?text=No+Image'">
            </div>
            <div class="product-detail-info">
                <div class="product-category">${product.category || 'Uncategorized'}</div>
                <h2>${product.name}</h2>
                <div class="product-price-large">$${parseFloat(product.price).toFixed(2)}</div>
                <p class="product-description-full">${product.description || 'No description available.'}</p>
                <div class="product-stock-info">
                    <i class="fas fa-box"></i>
                    <span>${product.stock} units available</span>
                </div>
                <button onclick="addToCart(${JSON.stringify(product).replace(/"/g, '&quot;')})" 
                        class="btn btn-primary btn-large" 
                        ${product.stock === 0 ? 'disabled' : ''}>
                    <i class="fas fa-cart-plus"></i> Add to Cart
                </button>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Add to cart
async function addToCart(product) {
    // For demo purposes, using a fixed user_id. In production, get from session/auth
    const userId = 1;
    
    try {
        const response = await fetch(`${API_URL}/cart`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                product_id: product.id,
                quantity: 1
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(`${product.name} added to cart!`, 'success');
            updateCartBadge();
            
            // Close modal if open
            document.getElementById('productModal').style.display = 'none';
        } else {
            showToast(data.error || 'Failed to add to cart', 'error');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('Failed to add to cart. Please try again.', 'error');
    }
}

// Update cart badge
async function updateCartBadge() {
    const userId = 1; // Demo user
    
    try {
        const response = await fetch(`${API_URL}/cart/${userId}`);
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

// Truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

