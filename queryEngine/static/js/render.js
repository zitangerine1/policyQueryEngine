function sleep(ms = 0) {
	return new Promise(resolve => setTimeout(resolve, ms));
}


$(document).ready(function() {
    // Attach a click event to the button
    $("#updateButton").click(function() {
        // Make an AJAX request to your Flask server
        $.ajax({
            type: "POST",
            url: "/sendmessage",  // Replace with your Flask route
            success: function(data) {
                // Check for success flag in the response
                if (data.success) {
									// Update the content of the specified div
									console.log("Received data:", data);
									$("#chatContainer").html(data.updated_content);
								} else {
									console.error("Error:", data.error);
								}
						},
					error: function(error) {
							console.error("Error:", error);
						}
				});
		});
});
