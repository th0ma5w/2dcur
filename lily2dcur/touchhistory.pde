PFont fontA = loadFont("Arial");
textFont(fontA, 8);
int theWidth = 400;
int theHeight = 400;



void setup() 
{
  size(theWidth, theHeight); 
  smooth();
  noStroke();
  background(0);
  fill(255,153);
  }

void draw(){
  noStroke();
  background(0);
  fill(255,153);
  stroke(255);
  noFill();
	for (x in ENV){
		thisEvent=ENV[x];
		beginShape();
		for (y in thisEvent){
			thisPoint=thisEvent[y];
			theX=thisPoint[0]*theWidth;
			theY=thisPoint[1]*theHeight;
			vertex(theX,theY);	
		}
		endShape();
		text(theX + ',' + theY,theX,theY);
	}
}

