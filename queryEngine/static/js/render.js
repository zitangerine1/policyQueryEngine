$(document).ready(function(){
  function fetchAllMessages() {
    var chatContainer = document.querySelector('#chatContainer')

    $.ajax({
      url: "/getallmessages",  // endpoint that returns all messages
      type: "GET",
      success: function(data) {
        $('#chatContainer').empty(); // clear the chat container
        $('#sourceBox').empty();

        data.forEach(function(chat_item){ // loop over each chat item message
          if (chat_item.sender == 'System Message') {
            var imgSource = "https://www.gstatic.com/lamda/images/sparkle_resting_v2_darkmode_2bdb7df2724e450073ede.gif";
          } else {
             var imgSource = "https://i1.sndcdn.com/artworks-csS0KMfy54ypqFXq-WTMOyg-t500x500.jpg";
          }

          var newMessageHTML = `
            <div class="flex items-start gap-2.5 mx-4 my-3 animate__animated animate__fadeIn">
              <img class="w-8 h-8 rounded-full" src="${imgSource}" alt="System image">
              <div class="flex flex-col w-full max-w-[90%] leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700">
                <div class="flex items-center space-x-2 rtl:space-x-reverse">
                  <span class="text-sm font-semibold text-gray-900 dark:text-white">${chat_item.sender}</span>
                  <span class="text-sm font-normal text-gray-500 dark:text-gray-400">${chat_item.time}</span>
                </div>
                <p class="text-sm font-normal py-2 text-gray-900 dark:text-white">
                  ${chat_item.message}
                </p>
              </div>
            </div>`;

          if (chat_item.source1 != undefined) {

            var sourceHTML = `
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Sources</h5>
            <p class="font-small text-gray-700 dark:text-gray-400">${chat_item.source1}</p><br>
            <p class="font-small text-gray-700 dark:text-gray-400">${chat_item.source2}</p><br>
            <p class="font-small text-gray-700 dark:text-gray-400">${chat_item.source3}</p>
          `
            $('#sourceBox').empty();
            $('#sourceBox').append(sourceHTML);
          }


          $('#chatContainer').append(newMessageHTML);

        });
      }
    });
  }

  var socket = io.connect("http://127.0.0.1:5000");

  socket.on('new_message', function(msg) {
    fetchAllMessages();
  })

});