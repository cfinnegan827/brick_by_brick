import {db, auth} from './firebaseConfig.js';
import { setDoc, doc, getDoc } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-firestore.js";
import { createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-auth.js";


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

        // Create user with Firebase Authentication
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        // Store additional user data in Firestore
        await setDoc(doc(db, 'users', username), {
            uid: user.uid,
            email: email,
            fullName: fullName,
            ownedSets: [], // Give user empty array of sets when registering
            wishlistSets: []
        });
        // Store username mapping for uniqueness check
        console.log('User created succesfully: ', username);

    } catch(error){
        console.error('Unable to create user: ', error);
        throw error;
    }
}

export{signup_user}