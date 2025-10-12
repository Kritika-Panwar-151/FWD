// script.js

document.addEventListener("DOMContentLoaded", function () {
    // Password toggle
    const toggleBtn = document.querySelector(".password-toggle");
    const passwordInput = document.getElementById("password");
    const eyeIcon = toggleBtn.querySelector(".eye-icon");

    toggleBtn.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            eyeIcon.classList.add("show-password");
        } else {
            passwordInput.type = "password";
            eyeIcon.classList.remove("show-password");
        }
    });

    // Login form submit simulation
    const loginForm = document.getElementById("loginForm");
    const loginBtn = document.querySelector(".login-btn");
    const btnText = loginBtn.querySelector(".btn-text");
    const btnLoader = loginBtn.querySelector(".btn-loader");

    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        // Show loading
        loginBtn.classList.add("loading");

        setTimeout(() => {
            loginBtn.classList.remove("loading");

            // Here you can do actual Django login post
            alert("Login successful (simulation)!");
        }, 1500);
    });
});
