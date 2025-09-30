
document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.menu-toggle'); // el botón hamburguesa
    const sidebar = document.querySelector('.sidebar'); // tu aside o nav
    const mainContent = document.querySelector('.main-content'); // el contenedor derecho

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
    });
});