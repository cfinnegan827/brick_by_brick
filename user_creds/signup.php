<?php
// Include Firebase SDK and configuration
require_once 'path/to/vendor/autoload.php';  // Include the Firebase SDK

use Firebase\Auth\Token\Exception\InvalidToken;
use Kreait\Firebase\Factory;
use Kreait\Firebase\ServiceAccount;

// Include Firebase configuration
$firebaseConfig = require_once 'firebaseConfig.php'; // Or use environment variables for Firebase credentials

$factory = (new Factory)
    ->withServiceAccount($firebaseConfig['serviceAccountJsonPath'])
    ->withDatabaseUri($firebaseConfig['databaseUri']);

// Initialize Firebase authentication
$auth = $factory->createAuth();

// Check if form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $fullName = $_POST['fullName'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';

    // Basic form validation
    if (empty($username) || empty($fullName) || empty($email) || empty($password)) {
        echo "All fields are required!";
        exit;
    }

    // Check if user already exists
    try {
        $existingUser = $auth->getUserByEmail($email);
        echo "User already exists!";
        exit;
    } catch (InvalidToken $e) {
        // No existing user, proceed with registration
    }

    // Create user in Firebase Authentication
    try {
        $userRecord = $auth->createUserWithEmailAndPassword($email, $password);

        // Once the user is created, you can store additional information like username and fullName
        $uid = $userRecord->uid;

        // Store user data in Firestore or Realtime Database
        $firestore = $factory->createFirestore();
        $userRef = $firestore->collection('users')->document($uid);

        // Add user info (username, fullName, email, and an empty list of sets)
        $userRef->set([
            'username' => $username,
            'fullName' => $fullName,
            'email' => $email,
            'sets' => []  // Empty list of sets for a new user
        ]);

        echo "User registered successfully!";
        // Redirect or provide login instructions
        header('Location: login.html');
        exit;

    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
}
?>
