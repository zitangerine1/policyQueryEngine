       
document.addEventListener('DOMContentLoaded', function() {
       document.getElementById('sendButton').addEventListener('click', function () {
              // Get the user's message from the input field
              let userMessage = document.getElementById('userMessageInput').value;

              // Check if the input is not empty before proceeding
              if (userMessage.trim() === '') {
                     alert('Please enter a message.');
                     return;          
              }

              // Create the message data
              let newData = {
                     'sender': 'User',
                     'time': new Date().toLocaleTimeString(),
                     'message': userMessage
              };

              // Send a POST request to the Flask route
              fetch('/sendmessage', {
                     method: 'POST',
                     headers: {
                            'Content-Type': 'application/json'
                     },
                     body: JSON.stringify(newData)
              })
        .then(response => response.json())
        .then(data => {
               // Update the conversation_data array with the received data
               conversation_data = data.conversation_data;

               // Handle the response if needed
               console.log(data);

               // You might also want to update your UI to reflect the new messages
               // For example, re-render the conversation with the updated conversation_data
        })
        .catch(error => {
               console.error('Error:', error);
        });
       });
});
