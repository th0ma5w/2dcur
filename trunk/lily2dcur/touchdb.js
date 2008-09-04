/*
* (c) 2008 Thomas Winningham winningham@gmail.com
*/
function $touchdb()
{
	var thisPtr=this;
	thisPtr.the_database={};

	this.inlet1=new this.inletClass("inlet1",this,"accepts finger list from tuio2dcur");
	this.inlet2=new this.inletClass("inlet2",this,"accepts coordinate updates from tuio2dcur");
	this.outlet1 = new this.outletClass("outlet1",this,"finger dictionary");
	this.outlet2 = new this.outletClass("outlet2",this,"finger added");
	this.outlet3 = new this.outletClass("outlet3",this,"finger updated");
	this.outlet4 = new this.outletClass("outlet4",this,"finger removed");
	this.outlet5 = new this.outletClass("outlet5",this,"finger x,y");
	this.outlet6 = new this.outletClass("outlet6",this,"starting touch finger x,y");
	this.outlet7 = new this.outletClass("outlet7",this,"ending touch finger x,y");
	
	this.inlet1["anything"]=function(msg) {
		msg=LilyUtils.splitArgs(msg);
		
		//iter the db looking for the finger id
		//first make all fingers 'new'
		old_fingers={}
		for (finger_id in msg){
			old_fingers[msg[finger_id]]=false;
		}
		//next make all the existing fingers up for removal
		finger_exists={}
		for (finger in thisPtr.the_database){
			finger_exists[finger]=false;
			
			//for each of those compare it to our new fingers
			for (finger_id in msg){
				if (finger==msg[finger_id]) {

					//now  this condition updates the mappings
					finger_exists[finger]=true;
					old_fingers[msg[finger_id]]=true;
				}
			}
		}
				
		//now remove those fingers in the db but not now active:
		thisPtr.removed_fingers=[]
		for (finger in finger_exists){
			if (finger_exists[finger] == false){
				thisPtr.outlet7.doOutlet([finger,thisPtr.the_database[finger]]);
				delete(thisPtr.the_database[finger]);
				thisPtr.removed_fingers.push(finger);
				}
			}
		//now make a list of the new fingers not seen before
		thisPtr.new_fingers=[];
		for (finger in old_fingers){
			if (old_fingers[finger]==false){
				thisPtr.new_fingers.push(finger);
			}
		}

	// only output if not empty
	if (thisPtr.new_fingers.length > 0) {
		thisPtr.outlet2.doOutlet(thisPtr.new_fingers);
		}
	if (thisPtr.removed_fingers.length > 0) {
		thisPtr.outlet4.doOutlet(thisPtr.removed_fingers);
	}

	return this;
	}
	
	this.inlet2["anything"]=function(msg){
	
		//for each finger update in the list, update the database
		msg=LilyUtils.splitArgs(msg);
		thisPtr.updated_fingers=[];
		for (finger in msg){
			fingerStats=LilyUtils.splitArgs(msg[finger]);
			finger_id=fingerStats.shift();
			if (thisPtr.the_database[finger_id]){
	
				//output only if the finger is different
				if (thisPtr.the_database[finger_id].join("") != fingerStats.join("")){
					//if previous exists
					oldstats=thisPtr.the_database[finger_id];
					if (oldstats){
						//calc the diff
						diffx=fingerStats[0]-oldstats[0];
						diffy=fingerStats[1]-oldstats[1];
					}
					thisPtr.the_database[finger_id]=fingerStats;
					thisPtr.updated_fingers.push([finger_id,fingerStats,[diffx,diffy]]);
				}
			}
			else {
					//this means that the finger doesn't exist in the db
                                        thisPtr.the_database[finger_id]=fingerStats;
                                        thisPtr.updated_fingers.push([finger_id,fingerStats,[0,0]]);
					thisPtr.outlet6.doOutlet([finger_id,fingerStats]);
			}
		}
	
	// if we have changed anything
	if (thisPtr.updated_fingers.length > 0){
		
		
		// output every updated finger
		for (finger in thisPtr.updated_fingers){
			thisPtr.outlet3.doOutlet(thisPtr.updated_fingers[finger]);
		}
	}

	// output just x&y of each finger when sequenced
	// output every finger in the database, recording each x,y
	thisPtr.finger_xy=[];
	for (fingerID in thisPtr.the_database){
			finger=thisPtr.the_database[fingerID];
			thisPtr.finger_xy.push([finger[0],finger[1]]);
			thisPtr.outlet1.doOutlet([fingerID,finger]);
	}
	if (thisPtr.finger_xy.length > 0){
			thisPtr.outlet5.doOutlet(thisPtr.finger_xy);
	}

	return this;
	}
	
}


//meta data module- required. the module name should take the form "$"+ classname/filename +"MetaData"
var $touchdbMetaData = {
	textName:"touchdb", //the name as it will appear to the user- can be different from the filename/classname
	htmlName:"touchdb", //same as above, but valid for an xhtml document with appropriate entity substitutions. 
	objectCategory:"TUIO", //where to file, need not be an existing category
	objectSummary:"Maintain a dictionary of finger touches.", //one sentence description for help system
	objectArguments:"" //also for help- object argument list if any, otherwise empty.
}
