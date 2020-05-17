function loadingScreen() {
    document.getElementById("container").innerHTML = `<!-- LOADING -->
    <div class="loader loader--style1" title="0" style="margin-top: 10vh;">
        <svg version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        width="120px" height="120px" viewBox="0 0 40 40" enable-background="new 255 255 255 255" xml:space="preserve">
        <path opacity="1.0" fill="#FFFFFF" d="M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946
        s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634
        c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z"/>
        <path fill="#000" d="M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0
        C22.32,8.481,24.301,9.057,26.013,10.047z">
        <animateTransform attributeType="xml"
            attributeName="transform"
            type="rotate"
            from="0 20 20"
            to="360 20 20"
            dur="0.5s"
            repeatCount="indefinite"/>
        </path>
        <p style="font-size: 5em">Finding players...</p>
        </svg>
    </div>`;
}

function changeToDraw(category) {
    var toDraw = document.getElementById("todraw");
    toDraw.innerHTML = category;
}

//Ai reply in the footer
function aiReply(reply) {
    document.getElementById("ai").innerHTML = reply;
}

//SKip category
function skip() {
    socket.send("skip");
}

//Load main game UI
function game() {
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
                <div>
                    <p>erase</p>
                </div>
                <div onClick="skip()">
                    <p>skip</p>
                </div>
                <div>
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
