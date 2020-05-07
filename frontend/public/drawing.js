/* construct manually */
var bar1 = new ldBar("#opponent1");
/* ldBar stored in the element */
var bar2 = document.getElementById('opponent1').ldBar;
bar1.set(60);

var canvas;
var socket;

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function setup() {
  canvas = createCanvas(windowWidth, windowHeight);
  canvas.position(0, 0);

  background(255);

  socket = io.connect('http://localhost:3000');
  socket.on('mouse', newDrawing);
}

function newDrawing(data) {
  strokeWeight(4);
  stroke(255, 100, 100);
  line(data.px, data.py, data.x, data.y);
}

function draw() {

  var data = {
    px: pmouseX,
    py: pmouseY,
    x: mouseX,
    y: mouseY
  }

  if(mouseIsPressed) {

    if(mouseButton === LEFT) {
      socket.emit('mouse', data);
      stroke(0);
      strokeWeight(4);
      line(pmouseX, pmouseY, mouseX, mouseY);
    }

    else if (mouseButton === RIGHT) {
      background(255);
    }
  }
}
