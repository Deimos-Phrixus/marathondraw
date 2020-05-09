const socket = new WebSocket('ws://localhost:8080');

//Connection apple
socket.onopen = function(e) {
  document.title = "Connection established";
  console.log("[open] connected")
  document.title = "Sending to server";
  socket.send("BEGIN");
  console.log("[sent] initial message sent")
  document.title = "Connected";
  
};

//Server message recieved
socket.onmessage = function(event) {
  console.log('[message] Data received from server: '+ event.data);
};

//Connection closure
socket.onclose = function(event) {
  if (event.wasClean) {
    document.title = "Closed cleanly";
    console.log("[close] Event code: "+event.code+"   reason: "+event.reason);
  } else {
    document.title = "Closed badly";
  }
};

//Error handler
socket.onerror = function(error) {
  console.log("[error] "+error.message);
};
