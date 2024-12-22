document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add loading state to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.getAttribute('href') && !this.getAttribute('href').startsWith('#')) {
                this.classList.add('disabled');
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });
});

// Error handling for images
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
        this.src = 'https://via.placeholder.com/150?text=No+Image';
    });
});
