const cart = {};

document.querySelectorAll('.increase').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.dataset.id;
        const quantityCell = document.getElementById(`quantity-${productId}`);
        let currentQuantity = parseInt(quantityCell.textContent) || 0;
        currentQuantity += 1;
        quantityCell.textContent = currentQuantity;

        updateCart(productId, currentQuantity);
    });
});

document.querySelectorAll('.decrease').forEach(button => {
    button.addEventListener('click', function () {
        const productId = this.dataset.id;
        const quantityCell = document.getElementById(`quantity-${productId}`);
        let currentQuantity = parseInt(quantityCell.textContent) || 0;

        if (currentQuantity > 0) {
            currentQuantity -= 1;
            quantityCell.textContent = currentQuantity;
            updateCart(productId, currentQuantity);
        }
    });
});

function updateCart(productId, quantity) {
    if (quantity > 0) {
        cart[productId] = { quantity: quantity };
    } else {
        delete cart[productId];
    }
    displayCart();
}

function displayCart() {
    const cartItems = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    cartItems.innerHTML = '';
    let totalCount = 0;

    for (const productId in cart) {
        const item = cart[productId];
        const li = document.createElement('li');
        li.textContent = `Product ID ${productId} - Quantity: ${item.quantity}`;
        cartItems.appendChild(li);
        totalCount += item.quantity;
    }

    cartCount.textContent = totalCount;
}

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    // Here you would typically send the login data to the server using fetch or axios.
    // For demonstration, we'll just display a message.

    if (username === "test" && password === "password") { // Replace with your validation logic
        document.getElementById("message").textContent = "Login successful!";
        document.getElementById("message").style.color = "green";
    } else {
        document.getElementById("message").textContent = "Invalid username or password.";
    }
});
document.getElementById('profileDropdown').addEventListener('click', function(event) {
    const dropdownContent = document.getElementById('dropdownContent');
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    event.stopPropagation(); // Prevent event from bubbling up
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function() {
    const dropdownContent = document.getElementById('dropdownContent');
    dropdownContent.style.display = 'none';
});
