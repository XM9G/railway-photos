document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const linkLists = document.querySelectorAll('ul'); // Select all <ul> elements
    const allLinks = document.querySelectorAll('ul a');

    searchInput.addEventListener('input', function () {
        const searchTerm = searchInput.value.trim().toLowerCase();

        allLinks.forEach(link => {
            const linkText = link.textContent.toLowerCase();
            const linkHref = link.href.toLowerCase();

            if (linkText.includes(searchTerm) || linkHref.includes(searchTerm)) {
                link.parentElement.style.display = 'block';
            } else {
                link.parentElement.style.display = 'none';
            }
        });
    });
});