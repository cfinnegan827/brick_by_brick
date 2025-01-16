import {db, auth} from './firebaseConfig.js';
import {doc, getDoc } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-firestore.js";
import { signInWithEmailAndPassword,signOut } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-auth.js";


async function login_user(username, password) {
    try {
        const userRef = doc(db, 'users', username);
        const userSnap = await getDoc(userRef);

        if (!userSnap.exists()) {
            throw new Error('User not found');
        }
        const userData = userSnap.data();
        const email = userData.email;

        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const authUser = userCredential.user;

        // After successful Firebase login, send data to the backend
        const response = await fetch('/set-cookies', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                ownedSets: userData.ownedSets,
                wishlist: userData.wishlistSets,
            }),
        });

        console.log('Login successful:', username);
        return authUser; // Return the authenticated user object if needed
    } catch (error) {
        console.error('Login failed:', error.message);
        throw error;
    }
}


export {login_user}