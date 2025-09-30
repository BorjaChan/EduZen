document.addEventListener("DOMContentLoaded", function () {
    const btnLogin = document.getElementById('btnLogin');
    const btnRegister = document.getElementById('btnRegister');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    btnLogin.addEventListener('click', () => {
        loginForm.classList.remove('oculto');
        registerForm.classList.add('oculto');
    });

    btnRegister.addEventListener('click', () => {
        registerForm.classList.remove('oculto');
        loginForm.classList.add('oculto');
    });
});
