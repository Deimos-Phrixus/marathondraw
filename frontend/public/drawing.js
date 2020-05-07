/* construct manually */
var bar1 = new ldBar("#opponent1");
/* ldBar stored in the element */
var bar2 = document.getElementById('opponent1').ldBar;
bar1.set(60);

var canvas;
var socket;

function windowResized() {
  resizeCanvas(window.innerWidth, window.innerHeight);
  background('#2f2f2f');
}

function setup() {
  canvas = createCanvas(window.innerWidth, window.innerHeight);
  canvas.position(0, 0);

  background('#2f2f2f');

  socket = io.connect('http://localhost:3000');
  socket.on('mouse', newDrawing);
}

function newDrawing(data) {
  stroke('#e8e8e8');
  strokeWeight(4);
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
      stroke('#e8e8e8');
      line(pmouseX, pmouseY, mouseX, mouseY);
    }

    else if (mouseButton === RIGHT) {
      background('#2f2f2f');
    }
  }
}
