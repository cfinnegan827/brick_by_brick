import {db  } from './firebaseConfig.js';
import { setDoc } from "https://www.gstatic.com/firebasejs/9.1.3/firebase-firestore.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.1.3/firebase-auth.js";


//singup functions
async function signup_user(username, email, password, fullName){
    try{
        // Check if the username is already taken
        const usernameRef = doc(db, 'usernames', username);
        const usernameSnap = await getDoc(usernameRef);

        if (usernameSnap.exists()) {
            console.error('Username already taken');
            throw new Error('Username already taken');
        }

        const auth = getAuth();
        // Create user with Firebase Authentication
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        // Store additional user data in Firestore
        await setDoc(doc(db, 'users', user.uid), {
            username: username,
            email: email,
            fullName: fullName,
            ownedSets: [], // Give user empty array of sets when registering
            wishlistSets: []
        });
        // Store username mapping for uniqueness check
        await setDoc(usernameRef, { uid: user.uid });
        console.log('User created succesfully: ', docRef);

    } catch(error){
        console.error('Unable to create user: ', error);
        throw error;
    }
}

export{signup_user}