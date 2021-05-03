createCheckoutSession = function (userId) {
    const stripe = Stripe("pk_test_51IMONzIkAX7cDP9r31eBOkpKbLQ7B99gzod9hRZMLonM5zSQEhoYdUEVYXRvp7rQpztlMyNTM9sR7Cxez5R0XMFa0038JCwaoH");
    const startPayment = "https://stripepaymentmanagement.azurewebsites.net/api/CreateSubscription?code=weGCE9v2UaKuWykFCMy9bwj6aYxRMgraKQXW/ZrPT9Bz5lhCBeGTeA==&userId=" + userId;
    return fetch(startPayment, {
        method: "POST"
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            return stripe.redirectToCheckout({ sessionId: session.id });
        })
        .then(function (result) {
            // If redirectToCheckout fails due to a browser or network
            // error, you should display the localized error message to your
            // customer using error.message.
            if (result.error) {
                alert(result.error.message);
            }
        })
        .catch(function (error) {
            console.error("Error:", error);
        });
}