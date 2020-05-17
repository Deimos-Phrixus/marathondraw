//Loading screen for matchmaking. https://codepen.io/aurer/pen/jEGbA
function loadingScreen() {
    document.getElementById("container").innerHTML = `<!-- LOADING 4 -->
    <div class="loader loader--style4" title="3" id="loadingScreen">
      <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
         width="24px" height="24px" viewBox="0 0 24 24" style="enable-background:new 0 0 50 50;" xml:space="preserve">
        <rect x="0" y="0" width="4" height="7" fill="#333">
          <animateTransform  attributeType="xml"
            attributeName="transform" type="scale"
            values="1,1; 1,3; 1,1"
            begin="0s" dur="0.6s" repeatCount="indefinite" />       
        </rect>

        <rect x="10" y="0" width="4" height="7" fill="#333">
          <animateTransform  attributeType="xml"
            attributeName="transform" type="scale"
            values="1,1; 1,3; 1,1"
            begin="0.2s" dur="0.6s" repeatCount="indefinite" />       
        </rect>
        <rect x="20" y="0" width="4" height="7" fill="#333">
          <animateTransform  attributeType="xml"
            attributeName="transform" type="scale"
            values="1,1; 1,3; 1,1"
            begin="0.4s" dur="0.6s" repeatCount="indefinite" />       
        </rect>
      </svg>
    </div>`;
}

//Load main game UI
function gameScreen() {
    //Delete loadingscreen div before showing UI
    var ldscreen = document.getElementById('loadingScreen');
    ldscreen.parentNode.removeChild(ldscreen);

    var imported = document.createElement('script');
    imported.src = 'libraries/p5.js';
    document.head.appendChild(imported);
    imported = document.createElement('script');
    imported.src = 'drawing.js';
    document.head.appendChild(imported);

    document.getElementById("container").innerHTML = `<div id="topUI">
        <div id="info">
            <div>
                <p id="todraw">draw: snake</p>
            </div>
            <div>
                <p>60</p>
            </div>
            <div id="options">
                <div onClick="skip()">
                    <p>skip</p>
                </div>
                <div onClick="quit()">
                    <p>quit</p>
                </div>
            </div>
        </div>
    </div>
    <div id="paint"></div>
    <footer>
        <p id="ai">snake?</p>
    </footer>`;
}


//Change category to draw
function changeToDraw(category) {
    var toDraw = document.getElementById("todraw");
    toDraw.innerHTML = "draw: " + category;
}

//Asyncronous countdown
//https://stackoverflow.com/questions/50041474/javascript-countdown-timer-for-hour-minutes-and-seconds-when-a-start-button-cli
function countdownMatch(limit) {
    // Countdown
    var x = setInterval(function (limit) {
        var seconds = Math.floor((limit % (1000 * 60)) / 1000);

        document.getElementById("countdown").innerHTML = seconds;

        // If the count down is finished, write some text
        if (seconds < 0) {
            socket.send("finish");
        }
    }, 1000);
}

//Ai reply in the footer
function aiReply(reply) {
    document.getElementById("ai").innerHTML = reply;
}

//Skip category
function skip() {
    socket.send("skip");
}

//Quit game
function skip() {
    socket.send("finished");
}
