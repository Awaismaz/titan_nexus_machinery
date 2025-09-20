document.addEventListener('DOMContentLoaded', () => {
    const yearPlaceholder = document.querySelectorAll('[data-current-year]');
    yearPlaceholder.forEach(node => node.textContent = new Date().getFullYear());
});
