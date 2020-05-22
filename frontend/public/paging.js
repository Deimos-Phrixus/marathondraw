var countdown;
var countdownPaused = false;

//Loading screen for matchmaking. https://codepen.io/aurer/pen/jEGbA

function waitingPlayersScreen() {
    loadSvg("Wait for others to finish...");
}

function scoreboardScreen(data) {
    // 4, 4, 3,4,5,6, 2,3,4,5
    data = data.split(",")
    winner = data[2];
    htmlString = `
        <div>
        <h1> Winner: ` + winner + ` </h1>`
    for (var i = 0; i < int(data[1]); i += 1) {
        htmlString += "<p> " + data[2 + i] + " : " + data[2 + int(data[1]) + i] + " </p>";
    }
    htmlString += `<a href="/">Play agian? </a>`
    htmlString += "</div>"
    document.getElementById("container").innerHTML = htmlString;
}

function loadSvg(msg) {
    document.getElementById("container").innerHTML = `<!-- LOADING 4 -->
    <div class="loader loader--style4" title="3" id="loadingScreen">
      <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
         width="100px" height="100px" viewBox="0 0 24 24" style="enable-background:new 0 0 50 50;" xml:space="preserve">
        <rect x="0" y="0" width="4" height="7" fill="#fff">
          <animateTransform  attributeType="xml"
            attributeName="transform" type="scale"
            values="1,1; 1,3; 1,1"
            begin="0s" dur="0.6s" repeatCount="indefinite" />
        </rect>

        <rect x="10" y="0" width="4" height="7" fill="#fff">
          <animateTransform  attributeType="xml"
            attributeName="transform" type="scale"
            values="1,1; 1,3; 1,1"
            begin="0.2s" dur="0.6s" repeatCount="indefinite" />
        </rect>
        <rect x="20" y="0" width="4" height="7" fill="#fff">
          <animateTransform  attributeType="xml"
            attributeName="transform" type="scale"
            values="1,1; 1,3; 1,1"
            begin="0.4s" dur="0.6s" repeatCount="indefinite" />
        </rect>
      </svg>
      <h3>` + msg + "</h3></div>";
}

function loadingScreen() {
    loadSvg("Finding Players...")
}

//Load main game UI
function gameScreen() {
    console.log("Initialising game screen");
    countdown = 60; // 60 seconds
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
                <p id="timer">60</p>
            </div>
            <div id="options">
                <div onClick="skip()" style="margin-right:10px;">
                    <p>skip  </p>
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

    startCountdown();
    updateCountdown();
}


//Change category to draw
function changeToDraw(category) {
    var toDraw = document.getElementById("todraw");
    toDraw.innerHTML = "draw: " + category;
}

//Asyncronous countdown
//https://stackoverflow.com/questions/50041474/javascript-countdown-timer-for-hour-minutes-and-seconds-when-a-start-button-cli
// function countdownMatch(limit) {
//     // Countdown
//     var x = setInterval(function (limit) {

//         countdown--;

//         var seconds = Math.floor((limit % (1000 * 60)) / 1000);

//         document.getElementById("countdown").innerHTML = seconds;

//         // If the count down is finished, write some text
//         if (seconds < 0) {
//             socket.send("finish");
//         }
//     }, 1000);
// }

function startCountdown() {
    var interval = setInterval(function () {
        if (!countdownPaused) {
            countdown--;
        }
        if (countdown == 0) {
            quit();
            clearInterval(interval);
        }
        updateCountdown();
    }, 1000);
}

function updateCountdown() {
    document.getElementById("timer").innerHTML = countdown;
}

//Ai reply in the footer
function aiReply(reply) {
    document.getElementById("ai").innerHTML = reply;
}

//Skip category
function skip() {
    socket.send("skip");
    // resetBackground();
}

//Quit game
function quit() {
    socket.send("finished");
    // resetBackground();
}
