var countdown;
var countdownPaused = false;

//Loading screen for matchmaking. https://codepen.io/aurer/pen/jEGbA

function waitingPlayersScreen() {
    loadSvg("Wait for others to finish...");
}

function scoreboardScreen(data) {
    BGchanger = `<script>
        // Code brought and modified from 
        // Ivang G. https://codepen.io/Zyxoman/pen/XZrJXz
        
        var x1 = 0;
        var y1 = 0;
        var z1 = 0;
        var x2;
        var y2;
        var z2;
        var x;
        var y;
        var z;
        var i = 0;

        function change() {
            document.getElementById("trophy").style.backgroundColor = \`rgb(\${x},\${y},\${z})\`;
        }

        function looper(k) {
            setTimeout(function() {
                x = Math.round(x1 + (k % 25) * (x2 - x1) / 25);
                y = Math.round(y1 + (k % 25) * (y2 - y1) / 25);
                z = Math.round(z1 + (k % 25) * (z2 - z1) / 25);
                change();
                //  document.body.innerHTML+=\`\${k}\` +" " + \`rgb(\${x1},\${y1},\${z1})\`  +" "+\`rgb(\${x2},\${y2},\${z2})\`  +" "+\`rgb(\${x},\${y},\${z})\`+"<br>";
            }, 0)
            i++;
            setTimeout(function() {
                number();
            }, 40)
        }

        function number() {
            //if (i<1500) { 
            if (i >= 0) {
                if (i >= 25 && ((i % 25) == 0)) {
                    x1 = x2;
                    y1 = y2;
                    z1 = z2;
                }
                if ((i % 25) == 0) {
                    x2 = Math.round(Math.random() * 255);
                    y2 = Math.round(Math.random() * 255);
                    z2 = Math.round(Math.random() * 255);

                }
                looper(i);
            }
        }

    </script>`;
    // 4, 4, 3,4,5,6, 2,3,4,5
    data = data.split(",")
    winner = data[2];
    htmlString = BGchanger;
    htmlString += `
        <div id="scoreboard">
        <div id="trophy"><h1>The winner is ` + winner + ` </h1></div>`;
    /*for (var i = 0; i < int(data[1]); i += 1) {
        htmlString += "<div id='trophy"+(i+1)+"'><p> " + data[2 + i] + " > " + data[2 + int(data[1]) + i] + " </p></div>";
    }
    htmlString += `<a href="/">Play again? </a>`;*/
    htmlString += "</div>";
    document.getElementById("container").innerHTML = htmlString;
    number();
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
