import {signup_user} from './signup_helper.js'; // Import the signup function

// Handle form submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('signup-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form values
        const username = document.getElementById('username').value.trim();
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        console.log(username);

        try {
            // Call the signup function
            await signup_user(username, email, password, fullName);
            messageDiv.textContent = 'Signup successful! Welcome, ' + username;
            messageDiv.style.color = 'green';
            form.reset(); // Clear the form
        } catch (error) {
            console.error('Error signing up:', error);
            messageDiv.textContent = 'Signup failed: ' + error.message;
            messageDiv.style.color = 'red';
        }
    });
});
