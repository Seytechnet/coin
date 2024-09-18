window.addEventListener('load', function() {
    var indexUrl = window.indexUrl; 

    // Select all elements with the class 'walletBtn'
    document.querySelectorAll('.walletBtn').forEach(function(button) {
        button.addEventListener('click', function() {
            window.location.href = indexUrl;
        });
    });
});