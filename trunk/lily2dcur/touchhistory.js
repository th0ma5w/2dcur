/*
* (c) 2008 Thomas Winningham winningham@gmail.com
*/
function $touchhistory()
{
	var thisPtr=this;
	thisPtr.the_database={};
	
	this.inlet1=new this.inletClass("inlet1",this,"touchdb finger add");
	this.inlet2=new this.inletClass("inlet2",this,"touchdb finger update");
	this.inlet3=new this.inletClass("inlet3",this,"touchdb finger remove");
	this.outlet1 = new this.outletClass("outlet1",this,"history database");
	
	this.inlet1["anything"]=function(msg) {
		for (id in msg) {
			thisPtr.the_database[msg[id]]=[];
		}
		return this;
	}
	
	this.inlet2["anything"]=function(msg) {
		existing_array=thisPtr.the_database[msg[0]];
		if (existing_array){
			existing_array.push(msg[1]);
		}else{
			existing_array=[msg[1]];
		}
		thisPtr.the_database[msg[0]]=existing_array;
		thisPtr.outlet1.doOutlet(thisPtr.the_database);
		return this;
	}

	this.inlet3["anything"]=function(msg) {
		for (id in msg) {
			if(thisPtr.the_database[msg[id]]){
				delete(thisPtr.the_database[msg[id]]);
			}
		}
		thisPtr.outlet1.doOutlet(thisPtr.the_database);
		return this;
	}
/*
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
		thisPtr.outlet1.doOutlet(thisPtr.fingerList);
		thisPtr.outlet2.doOutlet(thisPtr.fingerCoords);
	}	
return this;
}
*/
}

//meta data module- required. the module name should take the form "$"+ classname/filename +"MetaData"
var $touchhistoryMetaData = {
	textName:"touchhistory", //the name as it will appear to the user- can be different from the filename/classname
	htmlName:"touchhistory", //same as above, but valid for an xhtml document with appropriate entity substitutions. 
	objectCategory:"TUIO", //where to file, need not be an existing category
	objectSummary:"Process TUIO 2D cursor messages.", //one sentence description for help system
	objectArguments:"" //also for help- object argument list if any, otherwise empty.
}
