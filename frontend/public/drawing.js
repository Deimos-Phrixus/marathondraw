//Disable right click context menu that causes a stroke width bug
window.addEventListener('contextmenu', function (e) {
  e.preventDefault();
}, false);

var canvas;

function windowResized() {
  resizeCanvas(window.innerWidth, window.innerHeight);
  background('#2f2f2f');
}

function setup() {
  canvas = createCanvas(window.innerWidth, window.innerHeight);
  canvas.position(0, 0);

  background('#2f2f2f');
}

function draw() {
  loadPixels();

  var data = {
    px: pmouseX,
    py: pmouseY,
    x: mouseX,
    y: mouseY
  }

  if(mouseIsPressed) {
    if(mouseButton === LEFT) {
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
