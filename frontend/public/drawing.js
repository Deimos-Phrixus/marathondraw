//Disable right click context menu that causes a stroke width bug
window.addEventListener('contextmenu', function (e) {
  e.preventDefault();
}, false);

var canvas;

function windowResized() {
  resizeCanvas(window.innerWidth, window.innerHeight);
}

function setup() {
  canvas = createCanvas(window.innerWidth, window.innerHeight);
  canvas.position(0, 0);
}

function draw() {

  if(mouseIsPressed) {
    if(mouseButton === LEFT) {
      stroke('#e8e8e8');
      //Stroke backup algorithm >>> parseInt(Math.log((Math.sqrt(Math.pow((mouseX-pmouseX), 2)+Math.pow((mouseY-pmouseY), 2))))/Math.log(1.6)) + 2
      var distance = parseInt(Math.pow((Math.pow((mouseX-pmouseX), 2)+Math.pow((mouseY-pmouseY), 2)), 0.3)) + 4;
      strokeWeight(distance);
      line(pmouseX, pmouseY, mouseX, mouseY);
    }

    else if (mouseButton === RIGHT) {
      background('#2f2f2f');
    }
  }

  loadPixels();
}

function mouseReleased() {
  if(mouseButton === LEFT) {
    if(socket.readyState == 1)
    {
        var compressedPixels = compressPixels();
        socket.send("drawing");
        socket.send(width + "," + height);
        socket.send(compressedPixels.toString());
    }
  }
}

function compressPixels() {
  var compressedPixels = [];
  var i = 0;
  while(i < pixels.length) {
    if(pixels[i] < 50) {
      //0 is the background
      compressedPixels.push(0);
    }
    else{
      // 1 is the stroke
      compressedPixels.push(1);
    }

    i += 4;
  }

  return compressedPixels;
}
