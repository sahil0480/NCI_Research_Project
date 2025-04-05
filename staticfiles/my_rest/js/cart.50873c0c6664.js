// JavaScript function to handle adding items to the cart
function addToCart(itemId) {
    // Send an AJAX request to the server to add the item to the cart
    $.ajax({
        url: '/add-to-cart/',  // URL of the view that handles adding items to the cart
        type: 'POST',  // HTTP method
        data: {
            'item_id': itemId,  // ID of the item being added to the cart
            'csrfmiddlewaretoken': '{{ csrf_token }}'  // CSRF token to prevent CSRF attacks
        },
        success: function(response) {
            // If the request is successful, display a success message
            alert('Item added to cart!');
        },
        error: function(xhr, status, error) {
            // If the request fails, display an error message
            alert('Error adding item to cart');
        }
    });
}
