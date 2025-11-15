const API_URL = 'http://127.0.0.1:5000/api';
let currentProductId = null;
let deleteProductId = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    
    // Modal controls
    const modal = document.getElementById('productFormModal');
    const deleteModal = document.getElementById('deleteModal');
    const closeBtn = modal.querySelector('.close');
    
    document.getElementById('addProductBtn').addEventListener('click', () => openProductModal());
    closeBtn.addEventListener('click', () => closeProductModal());
    document.getElementById('cancelBtn').addEventListener('click', () => closeProductModal());
    document.getElementById('productForm').addEventListener('submit', saveProduct);
    
    // Delete modal controls
    document.getElementById('cancelDeleteBtn').addEventListener('click', () => {
        deleteModal.style.display = 'none';
        deleteProductId = null;
    });
    document.getElementById('confirmDeleteBtn').addEventListener('click', confirmDelete);
    
    // Close modals on outside click
    window.onclick = (e) => {
        if (e.target == modal) closeProductModal();
        if (e.target == deleteModal) {
            deleteModal.style.display = 'none';
            deleteProductId = null;
        }
    };
});

// Load products
async function loadProducts() {
    const loading = document.getElementById('loading');
    const tbody = document.getElementById('productsTableBody');
    
    try {
        loading.style.display = 'block';
        
        const response = await fetch(`${API_URL}/products`);
        const data = await response.json();
        
        if (response.ok) {
            const products = data.products || [];
            displayProducts(products);
        } else {
            showToast(data.error || 'Failed to load products', 'error');
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showToast('Failed to load products. Please try again.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display products in table
function displayProducts(products) {
    const tbody = document.getElementById('productsTableBody');
    
    if (products.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-table">
                    <i class="fas fa-inbox"></i>
                    <p>No products yet. Click "Add New Product" to get started!</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = products.map(product => {
        const imageUrl = product.image_url || 'https://via.placeholder.com/60x60?text=No+Image';
        const stockClass = product.stock === 0 ? 'out-of-stock' : (product.stock < 10 ? 'low-stock' : 'in-stock');
        
        return `
            <tr>
                <td>
                    <img src="${imageUrl}" alt="${product.name}" class="table-image" 
                         onerror="this.src='https://via.placeholder.com/60x60?text=No+Image'">
                </td>
                <td>
                    <div class="product-name-cell">${product.name}</div>
                    <div class="product-desc-cell">${truncateText(product.description, 60)}</div>
                </td>
                <td>${product.category || '-'}</td>
                <td class="price-cell">$${parseFloat(product.price).toFixed(2)}</td>
                <td>
                    <span class="stock-badge ${stockClass}">${product.stock}</span>
                </td>
                <td class="actions-cell">
                    <button onclick="editProduct(${product.id})" class="btn-icon btn-edit" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="deleteProduct(${product.id})" class="btn-icon btn-delete" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Open product modal for adding/editing
function openProductModal(product = null) {
    const modal = document.getElementById('productFormModal');
    const title = document.getElementById('modalTitle');
    const form = document.getElementById('productForm');
    
    // Reset form
    form.reset();
    document.getElementById('productId').value = '';
    currentProductId = null;
    
    if (product) {
        // Edit mode
        title.textContent = 'Edit Product';
        document.getElementById('productId').value = product.id;
        document.getElementById('productName').value = product.name;
        document.getElementById('productDescription').value = product.description || '';
        document.getElementById('productPrice').value = product.price;
        document.getElementById('productStock').value = product.stock;
        document.getElementById('productCategory').value = product.category || '';
        document.getElementById('productImage').value = product.image_url || '';
        currentProductId = product.id;
    } else {
        // Add mode
        title.textContent = 'Add New Product';
    }
    
    modal.style.display = 'block';
}

// Close product modal
function closeProductModal() {
    document.getElementById('productFormModal').style.display = 'none';
    document.getElementById('productForm').reset();
    currentProductId = null;
}

// Save product (add or update)
async function saveProduct(e) {
    e.preventDefault();
    
    const productData = {
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        price: parseFloat(document.getElementById('productPrice').value),
        stock: parseInt(document.getElementById('productStock').value),
        category: document.getElementById('productCategory').value,
        image_url: document.getElementById('productImage').value
    };
    
    try {
        let response;
        if (currentProductId) {
            // Update existing product
            response = await fetch(`${API_URL}/products/${currentProductId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        } else {
            // Create new product
            response = await fetch(`${API_URL}/products`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        }
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message || 'Product saved successfully!', 'success');
            closeProductModal();
            loadProducts();
        } else {
            showToast(data.error || 'Failed to save product', 'error');
        }
    } catch (error) {
        console.error('Error saving product:', error);
        showToast('Failed to save product. Please try again.', 'error');
    }
}

// Edit product
async function editProduct(productId) {
    try {
        const response = await fetch(`${API_URL}/products/${productId}`);
        const data = await response.json();
        
        if (response.ok) {
            openProductModal(data.product);
        } else {
            showToast(data.error || 'Failed to load product', 'error');
        }
    } catch (error) {
        console.error('Error loading product:', error);
        showToast('Failed to load product. Please try again.', 'error');
    }
}

// Delete product (show confirmation)
function deleteProduct(productId) {
    deleteProductId = productId;
    document.getElementById('deleteModal').style.display = 'block';
}

// Confirm delete
async function confirmDelete() {
    if (!deleteProductId) return;
    
    try {
        const response = await fetch(`${API_URL}/products/${deleteProductId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message || 'Product deleted successfully!', 'success');
            document.getElementById('deleteModal').style.display = 'none';
            deleteProductId = null;
            loadProducts();
        } else {
            showToast(data.error || 'Failed to delete product', 'error');
        }
    } catch (error) {
        console.error('Error deleting product:', error);
        showToast('Failed to delete product. Please try again.', 'error');
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

