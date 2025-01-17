import {login_user} from "./login_helper.js";

// Handle form submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form values
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        try {
            // Call the signup function
            await login_user(username, password);
            messageDiv.textContent = 'Login successful! Welcome, ' + username;
            messageDiv.style.color = 'green';
            form.reset(); // Clear the form
        } catch (error) {
            console.error('Error signing up:', error);
            messageDiv.textContent = 'login failed: ' + error.message;
            messageDiv.style.color = 'red';
        }
    });
});
