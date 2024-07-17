import { initializeApp, getApps } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// export const firebaseConfig = {
//     apiKey: process.env.FIREBASE_API_KEY,
//     authDomain: process.env.FIREBASE_AUTH_DOMAIN,
//     projectId: process.env.FIREBASE_PROJECT_ID,
//     storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
//     messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
//     appId: process.env.FIREBASE_APP_ID,
//     measurementId: process.env.FIREBASE_MEASUREMENT_ID,
// };

export const firebaseConfig = {
    apiKey: "AIzaSyBmOiWLgmWrKwdzHhb-7Y9GPFGzarUFvrg",
    authDomain: "nr-banesco.firebaseapp.com",
    projectId: "nr-banesco",
    storageBucket: "nr-banesco.appspot.com",
    messagingSenderId: "877846105040",
    appId: "1:877846105040:web:a423b6428951a20a22c7d5"
};

const firebaseApp = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const db = getFirestore(firebaseApp);
