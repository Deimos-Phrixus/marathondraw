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
      stroke('#e8e8e8');
      //Stroke backup algorithm >>> parseInt(Math.log((Math.sqrt(Math.pow((mouseX-pmouseX), 2)+Math.pow((mouseY-pmouseY), 2))))/Math.log(1.6)) + 2 
      var distance = parseInt(Math.pow((Math.pow((mouseX-pmouseX), 2)+Math.pow((mouseY-pmouseY), 2)), 0.3)) + 4;
      strokeWeight(distance);
      console.log(distance);
      line(pmouseX, pmouseY, mouseX, mouseY);
    }

    else if (mouseButton === RIGHT) {
      background('#2f2f2f');
    }
  }
}
