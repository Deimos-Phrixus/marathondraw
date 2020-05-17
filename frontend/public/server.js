const socket = new WebSocket('ws://localhost:5555');

var nickname = prompt("Nickname?", Math.floor(Math.random() * 100));

//Connection apple
socket.onopen = function (e) {
    document.title = "Connected";
    console.log("[open] connected")
    document.title = "Searching room...";
    socket.send("name," + nickname);

    console.log("[sent] initial message sent")
    document.title = "Connected";

};

//Server message recieved
socket.onmessage = function (event) {
    console.log('[message] Data received from server: ' + event.data);
    switch (event.data.split(",")[0]) {
        case "0": //Initial handshake
            console.log('Player connected and waiting.');
            loadingScreen();
            break;
        case "1": //Game started
            console.log('Game started and running.');
            game();
            break;
        case "2": //Drawing categories and predictions
            var code2 = event.data.split(",");

            if (code2[1] == "") {
                aiReply(code2[2] + "?")
            } else {
                if (code2.length == 3) {
                    aiReply("Correct!");
                    resetBackground();
                } else {
                    aiReply("Draw bitch!");
                }
                changeToDraw(code2[1]);
            }
            break;
    }
};

//Connection closure
socket.onclose = function (event) {
    if (event.wasClean) {
        document.title = "Closed cleanly";
        console.log("[close] Event code: " + event.code + "   reason: " + event.reason);
    } else {
        document.title = "Closed badly";
    }
};

//Error handler
socket.onerror = function (error) {
    console.log("[error] " + error.message);
};
