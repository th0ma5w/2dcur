/*
* (c) 2008 Thomas Winningham winningham@gmail.com
*/
function $touchspot(param)
{
	var thisPtr=this;
	var paramArr=LilyUtils.splitArgs(param);
 	        if(!paramArr.length) {
                LilyDebugWindow.error("The touchspot object needs arguments to be useful. Please specify x1, y1, x2, y2 as the bounding box, then width and height. The default is 0 0 1024 768 1024 768.");
                return;
        }

	var x1 = paramArr[0] 		|| 0;
	var y1 = paramArr[1] 		|| 0;
	var x2 = paramArr[2] 		|| 1024;
	var y2 = paramArr[3] 		|| 768;
	var width = paramArr[4] 	|| 1024;
	var height = paramArr[5] 	|| 768;

 
	
	this.inlet1=new this.inletClass("inlet1",this,"touchdb finger update fingerid, fingerstats");
	this.outlet1 = new this.outletClass("outlet1",this,"fingerid, fingerstats when touched");
	
	this.inlet1["anything"]=function(msg) {
		msgX=msg[1][0]*width;
		msgY=msg[1][1]*height;
		if (msgX >  x1) {
		if (msgY >  y1) {
		if (msgX <  x2) {
		if (msgY <  y2) {
			thisPtr.outlet1.doOutlet(msg);
		}
		}
		}
		}
		return this;
	}

}

//meta data module- required. the module name should take the form "$"+ classname/filename +"MetaData"
var $touchspotMetaData = {
	textName:"touchspot", //the name as it will appear to the user- can be different from the filename/classname
	htmlName:"touchspot", //same as above, but valid for an xhtml document with appropriate entity substitutions. 
	objectCategory:"TUIO", //where to file, need not be an existing category
	objectSummary:"Restrict TUIO 2D cursor messages to an area.", //one sentence description for help system
	objectArguments:"x1,y1,x2,y2,width,height" //also for help- object argument list if any, otherwise empty.
}
