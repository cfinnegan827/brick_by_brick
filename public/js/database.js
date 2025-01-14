import { db } from "../firebase/firebaseConfig";
import { doc, setDoc, getDoc } from "firebase/firestore";

// Add a LEGO set for a user
export const addSet = async (userId, setId, setName) => {
    const userDoc = doc(db, "users", userId);
    await setDoc(userDoc, {
        sets: {
            [setId]: setName,
        },
    }, { merge: true });
};

// Retrieve a user's sets
export const getSets = async (userId) => {
    const userDoc = doc(db, "users", userId);
    const snapshot = await getDoc(userDoc);
    return snapshot.exists() ? snapshot.data().sets : {};
};
