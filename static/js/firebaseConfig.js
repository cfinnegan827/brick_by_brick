import { initializeApp } from"https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBiPp6RiHTItm-Rouqc0G-OGCgfu2GpeLg",
  authDomain: "brick-by-brick-24317.firebaseapp.com",
  projectId: "brick-by-brick-24317",
  storageBucket: "brick-by-brick-24317.firebasestorage.app",
  messagingSenderId: "583153357550",
  appId: "1:583153357550:web:93f2d0b07548f9bf8899ff"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app)
export {db, auth};
