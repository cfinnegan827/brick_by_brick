import {db, auth} from '../../firebase/firebaseConfig';
import { doc, setDoc, getDoc} from 'firebase/firestore';
import { createUserWithEmailAndPassword } from 'firebase/auth';


//singup functions
async function signup_user(username, email, password, fullName){
    try{
        const userRef = doc(db, 'users', username);
        const userSnap = await getDoc(userRef);

        if(userSnap.exists()){
            console.error('Username already taken');
        }

        //if username isnt taken create a new user profile
        const userCredentials = await createUserWithEmailAndPassword(auth, email, password);

        await setDoc(userRef, {
            email: email,
            password: password,
            fullName: fullName,
            sets: [] //give user empty array of sets when registering
        });
        console.log('User created succesfully: ', username)
    } catch{
        console.error('Unable to create user: ', error.message)
    }
}

export{signup_user}