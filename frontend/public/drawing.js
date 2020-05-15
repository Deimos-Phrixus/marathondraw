//Disable right click context menu that causes a stroke width bug
window.addEventListener('contextmenu', function (e) {
  e.preventDefault();
}, false);

var canvas;
var lx, rx, ty, by;

function windowResized() {
  resizeCanvas(window.innerWidth, window.innerHeight);
}

function setup() {
  // pixelDensity(1);
  
  canvas = createCanvas(window.innerWidth, window.innerHeight);
  canvas.position(0, 0);
  background('#000000');
  lx = width;
  uy = height;
  rx = 0;
  by = 0;
  // rx, by = width, height;
}

var offsetx = 50
var offsety = 100

function draw() {

  if(mouseIsPressed) {
    if(mouseButton === LEFT) {
      stroke('#ffffff');
      //Stroke backup algorithm >>> parseInt(Math.log((Math.sqrt(Math.pow((mouseX-pmouseX), 2)+Math.pow((mouseY-pmouseY), 2))))/Math.log(1.6)) + 2
      var distance = parseInt(Math.pow((Math.pow((mouseX-pmouseX), 2)+Math.pow((mouseY-pmouseY), 2)), 0.3)) + 4;
      strokeWeight(5);
      line(pmouseX, pmouseY, mouseX, mouseY);
      lx = Math.min(lx, pmouseX-distance-10, mouseX-distance-offsetx);
      rx = Math.max(rx, pmouseX+distance+10, mouseX+distance+offsetx);
      uy = Math.min(uy, pmouseY-distance-10, pmouseY-distance-offsety);
      by = Math.max(by, pmouseY+distance+10, pmouseY+distance+offsety);
    }
    else if (mouseButton === RIGHT) {
      background('#000000');
      lx = width;
      uy = height;
      rx = 0;
      by = 0;
    }
  }

}

function mouseReleased() {
  loadPixels();

  if(mouseButton === LEFT) {
  }

}

function compressPixels() {
  var compressedPixels = [];
  console.log(pixels)
  var i = 0;
  var dim = Math.max(Math.abs(uy-by), Math.abs(lx-rx))
  var yadd = dim-Math.abs(uy-by)
  uy -= parseInt(yadd/2)
  by += yadd - parseInt(yadd/2)
  var xadd = dim-Math.abs(lx-rx)
  lx -= parseInt(xadd/2)
  rx += xadd - parseInt(xadd/2)
  

  // alert(uy)
  // alert(by)
  // alert(lx)
  // alert(rx)
  console.log(uy, by, lx, rx);
  for (y = uy; y < by; y++) {
    for (x = lx; x < rx; x++) {
      var p = get(x,y);
      var s = p[0] + p[1] + p[2];
      compressedPixels.push(s/3.0);
    }
  }
  // while(i ) {
  //   if(pixels[i] < 50) {
  //     //0 is the background
  //     compressedPixels.push(0);
  //   }
  //   else{
  //     // 1 is the stroke
  //     compressedPixels.push(1);
  //   }

  //   i += 4;
  // }

  return compressedPixels;
}

function keyPressed() {
  if (keyCode == ENTER) {
    var compressedPixels = compressPixels();
    if(socket.readyState == 1)
    {
        socket.send("drawing");
        socket.send(Math.abs(rx-lx) + "," + Math.abs(by-uy));
        // console.log(width + ","+ height);        
        socket.send(compressedPixels.toString());
        // console.log(compressedPixels.toString());        

    }
  }
}
