// auth.js
import { auth, db } from './firebaseConfig';  // Import Firebase authentication and Firestore
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";

// Handle user sign-up
document.getElementById('signup-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Create user with email and password using Firebase Auth
    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;

            // Save additional user data to Firestore
            setDoc(doc(db, "users", user.uid), {
                username: username,
                fullName: fullName,
                email: email,
                sets: []  // Empty list of sets initially
            })
                .then(() => {
                    console.log("User data saved to Firestore");
                    // Redirect to login page or dashboard
                    window.location.href = "/frontend/login.html";
                })
                .catch((error) => {
                    console.error("Error saving user data: ", error);
                });
        })
        .catch((error) => {
            console.error("Error signing up: ", error);
        });
});

// Handle login (you can also create a separate login form in `login.html`)
document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Sign in user with Firebase Auth
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            console.log("User logged in: ", user);
            // Redirect to dashboard or home page after successful login
            window.location.href = "/frontend/dashboard.html";
        })
        .catch((error) => {
            console.error("Error during login: ", error);
        });
});
