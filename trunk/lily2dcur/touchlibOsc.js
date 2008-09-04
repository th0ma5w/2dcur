/*
* (c) 2008 Thomas Winningham winningham@gmail.com
*/
function $touchlibOsc()
{
	var thisPtr=this;
	
	this.inlet1=new this.inletClass("inlet1",this,"accepts the output of oscreceive");
	this.outlet1 = new this.outletClass("outlet1",this,"finger list");
	this.outlet2 = new this.outletClass("outlet2",this,"finger coordinate messages");
	
this.inlet1["anything"]=function(msg) {
		//~ LilyDebugWindow.print(msg);
		if (msg.indexOf('2Dcur') > -1) {
		fseqSplit=msg.split(" fseq ");
		// LilyDebugWindow.print("fseqSplit0" + fseqSplit[0]);
		aliveSplit=fseqSplit[0].split(" alive ");
		//LilyDebugWindow.print("aliveSplit1 " + aliveSplit[0]);
		if (aliveSplit.length > 1){
		setSplit=aliveSplit[0].split(" set ");
		thisPtr.fingerList=aliveSplit[1].split(' ');
		setSplit.shift();
		thisPtr.fingerCoords=setSplit;
		thisPtr.fingerCount=setSplit.length;
		}
		else {
		thisPtr.fingerList=[];
		thisPtr.fingerCoords=[];
		}
		for (id in thisPtr.fingerCoords){
			thisPtr.fingerCoords[id][1]=1-thisPtr.fingerCoords[id][1];
		}
		thisPtr.outlet1.doOutlet(thisPtr.fingerList);
		thisPtr.outlet2.doOutlet(thisPtr.fingerCoords);
	}	
	return this;
	}
}

//meta data module- required. the module name should take the form "$"+ classname/filename +"MetaData"
var $touchlibOscMetaData = {
	textName:"touchlibOsc", //the name as it will appear to the user- can be different from the filename/classname
	htmlName:"touchlibOsc", //same as above, but valid for an xhtml document with appropriate entity substitutions. 
	objectCategory:"TUIO", //where to file, need not be an existing category
	objectSummary:"Process TUIO 2D cursor messages.", //one sentence description for help system
	objectArguments:"" //also for help- object argument list if any, otherwise empty.
}
