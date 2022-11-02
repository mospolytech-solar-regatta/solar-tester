listener_response = """
<!DOCTYPE html>
<html>
    <head>
        <title>Listen logs</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="subscribe(event)">
            <input type="text" id="topicName" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        
            var ws;
            function subscribe(event) {
                event.preventDefault();
                var input = document.getElementById("topicName")
                var endpoint = "ws://" + window.location.host + "/listen/" + input.value;
                ws = new WebSocket(endpoint);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    console.log(event.data);
                    if (event.data instanceof Blob) {
                        reader = new FileReader();
                
                        reader.onload = () => {
                            console.log("Result: " + reader.result);
                            content = document.createTextNode(reader.result)
                            message.appendChild(content)
                            messages.appendChild(message)
                        };
                
                        reader.readAsText(event.data);
                    } else {
                        message.appendChild(content)
                        messages.appendChild(message)
                    }
            
                };
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""