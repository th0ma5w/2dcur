/** 

Copyright (c) 2007 Bill Orcutt (http://lilyapp.org, http://publicbeta.cx)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

*/

/**
*	Construct a new helloworld object
*	@class
*	@constructor
*	@extends LilyObjectBase
*/
function $tuioSimulator()
{
	var thisPtr=this;
	
	this.inlet1=new this.inletClass("inlet1",this,"accepts the output of oscreceive");
	this.outlet1 = new this.outletClass("outlet1",this,"finger list");
	this.outlet2 = new this.outletClass("outlet2",this,"finger coordinate messages");
	
	this.inlet1["anything"]=function(msg) {
		// LilyDebugWindow.print(msg);
		if (msg.indexOf('2Dcur') > -1) {
		fseqSplit=msg.split(" fseq ");
		// LilyDebugWindow.print("fseqSplit0" + fseqSplit[0]);
		aliveSplit=fseqSplit[0].split(" alive ");
		//LilyDebugWindow.print("aliveSplit1 " + aliveSplit[0]);
		if (aliveSplit.length > 1){
		setSplit=aliveSplit[1].split(" set ");
		thisPtr.fingerList=setSplit.shift().split(' ');
		thisPtr.fingerCoords=setSplit;
		thisPtr.fingerCount=setSplit.length;
		}
		else {
		thisPtr.fingerList=[];
		thisPtr.fingerCoords=[];
		}
		thisPtr.outlet1.doOutlet(thisPtr.fingerList);
		thisPtr.outlet2.doOutlet(thisPtr.fingerCoords);
	}	
	return this;
	}
}

//meta data module- required. the module name should take the form "$"+ classname/filename +"MetaData"
var $tuioSimulatorMetaData = {
	textName:"tuioSimulator", //the name as it will appear to the user- can be different from the filename/classname
	htmlName:"tuioSimulator", //same as above, but valid for an xhtml document with appropriate entity substitutions. 
	objectCategory:"TUIO", //where to file, need not be an existing category
	objectSummary:"Process TUIO Simulator 2D cursor messages.", //one sentence description for help system
	objectArguments:"" //also for help- object argument list if any, otherwise empty.
}
