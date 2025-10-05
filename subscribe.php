<?php
/**
 * subscribe.php
 * Handles the email subscription form submission for Little Sprout.
 *
 * HOW IT WORKS:
 * 1. It only accepts POST requests with JSON data.
 * 2. It reads the incoming JSON to find the user's email address.
 * 3. It validates the email to make sure it's a real address.
 * 4. It constructs and sends an email notification to your specified address.
 * 5. It returns a success (200) or error (4xx, 5xx) message back to the website's JavaScript.
 */

// --- CONFIGURATION ---
// Set the email address where you want to receive subscription notifications.
$recipient_email = "lucian.mangu@gmail.com";

// Set the "from" address. For best results, use an email from your own domain.
// Many web hosts require this to prevent spam.
$sender_email = "noreply@littlesprout.ro"; 

// The subject line for the notification email you will receive.
$email_subject = "New Subscriber for Little Sprout!";
// --- END CONFIGURATION ---


// Set the content type of the response to JSON, so the browser understands it.
header("Content-Type: application/json");

// Only allow POST requests. If someone tries to access this file directly in their browser, it will show an error.
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405); // 405 Method Not Allowed
    echo json_encode(["message" => "Error: This script only accepts POST requests."]);
    exit();
}

// Get the raw data from the request body.
$json_data = file_get_contents('php://input');

// Decode the JSON data into a PHP object.
$data = json_decode($json_data);

// Check if the email field exists, is not empty, and is a valid email format.
if (!isset($data->email) || !filter_var($data->email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400); // 400 Bad Request
    echo json_encode(["message" => "Error: A valid email address is required."]);
    exit();
}

// Sanitize the user's email to prevent any malicious code injection.
$subscriber_email = htmlspecialchars($data->email);

// --- CONSTRUCT THE EMAIL ---
// This is the body of the email you will receive.
$email_body = "A new user has subscribed to the Little Sprout mailing list.\n\n";
$email_body .= "Email Address: " . $subscriber_email;

// These headers are important for the email to be sent correctly.
// The "From" header is required.
// The "Reply-To" header lets you click "Reply" in your email client to email the subscriber directly.
$headers = "From: Little Sprout <" . $sender_email . ">\r\n";
$headers .= "Reply-To: " . $subscriber_email . "\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

// --- SEND THE EMAIL ---
// The mail() function is a built-in PHP function. It relies on your web server's mailing system.
if (mail($recipient_email, $email_subject, $email_body, $headers)) {
    // If the email was sent successfully, return a success message.
    http_response_code(200); // 200 OK
    echo json_encode(["message" => "Thank you for subscribing!"]);
} else {
    // If the mail server failed, return a server error message.
    http_response_code(500); // 500 Internal Server Error
    echo json_encode(["message" => "Error: The server could not send the email. Please try again later."]);
}

?>
