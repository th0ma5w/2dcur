import liblo, math
#import pyglet, rabbyt

class touchList(list):
	"""a class that responds to OSC messages with TUIO data"""
	lastAlive=[]
	lastSet=[]
	def tuioAlive(self,pointsList):
		"""process the arguments of a TUIO Alive message"""
		for x in self:
			if x[0] not in pointsList:
				self.remove(x)
				self.statsRemove(x)
	def tuioSet(self,values):
		"""process a TUIO Set message"""
		self.append(values)
		self.statsUpdate(values)
	def handleOsc(self,path,args,types,src):
		"""OSC spawned event callback"""
		if args[0]=='alive':
			messages=args[1:len(args)]
			if messages != self.lastAlive:
				self.tuioAlive(messages)
				self.lastAlive=messages
		if args[0]=='set':
			messages=args[1:len(args)]
			if messages != self.lastSet:
				for x in self:
					if x[0]==args[1]:
						self.remove(x)
				self.tuioSet(args[1:len(args)])


class orienter(touchList):
	"""orient the touches to the display"""
	##osc
	#~ flipX=True
	#~ flipY=True
	#~ flipXDirection=True
	#~ flipYDirection=True
	#~ #TuioSimulator
	flipX=False
	flipY=True
	flipXDirection=False
	flipYDirection=True
	#-------------------------------------------------------------------
	def convert(self,x,y):
		"""convert a point"""
		w=self.window.width
		h=self.window.height
		if self.flipX:
			x=w-(x*w)
		else:
			x=x*w
		if self.flipY:
			y=h-(y*h)
		else:
			y=y*h
		return x,y
	def convertChange(self,x,y):
		"""convert a distance"""
		w=self.window.width
		h=self.window.height
		x,y = self.convert(x,y)
		if self.flipX:
			x=w-x
		if self.flipXDirection:
			x=-x
		if self.flipY:
			y=h-y
		if self.flipYDirection:
			y=-y
		return x,y



class touchStats(orienter):
	"""a class to hold observed stats about 2D cursor messages"""
	previously=[]
	eventStarts=[]
	differences=[]
	latest=[]
	lastDiff=[]
	start=False
	def calculateDifferences(self):
		"""calculate the distance between the current and previous updates"""
		for x in self.previously:
			if x[0]==self.latest[0]:
				then=x
				now=self.latest
				#~ if self.debug: print "then", then, "now", now
				thisDiff=(now[0],now[1]-then[1],now[2]-then[2])
				self.differences.append(thisDiff)
				self.lastDiff=thisDiff
	def determineStart(self):
		"""determine if we are processing an initial event"""
		self.start=True
		for x in self.previously:
			if x[0]==self.latest[0]:
				self.previously.remove(x)
				self.start=False
		self.previously.append(self.latest)
		if self.start:
			self.eventStarts.append(self.latest)
			self.lastDiff=[self.latest[0],0,0]
		#~ if self.debug: print "START",self.start
	def statsUpdate(self,values):
		"""update the internal stats with the given value"""
		self.latest=values
		#~ if self.debug: print "statsUpdate"
		#~ if self.debug: print self.latest
		#~ if self.debug: print self.previously
		#~ if self.debug: print self.eventStarts
		self.calculateDifferences()
		self.removeItem(self.differences,values[0])
		self.determineStart()
		#~ if self.debug: print self.latest
		#~ if self.debug: print self.previously
		#~ if self.debug: print self.eventStarts
		#
		# self.fingerUpdate() # to be overridden
		print "update", self.latest
	def removeItem(self,alist,ID):
		"""removes the latest event from the specified list"""
		#~ if self.debug: print "removeItem"
		for x in alist:
			if x[0]==ID:
				alist.remove(x)
	def statsRemove(self,finger):
		"""remove the specified values from the various lists"""
		#~ if self.debug: print "statsRemove",finger
		ID=finger[0]
		self.removeItem(self.eventStarts,ID)
		self.removeItem(self.differences,ID)
		self.removeItem(self.previously,ID)
		#~ if self.debug: print finger
		#~ if self.debug: print self.previously
		#~ if self.debug: print self.eventStarts
		#~ if self.debug: print self.differences
		#
		#self.fingerRemove(finger) #to be overridden
		print "remove", finger

class dummy:
	pass

class canvas(touchStats):
	"""main window"""
	#window=pyglet.window.Window()
	window=dummy()
	window.width=800
	window.height=600
	debug = False
	def redraw(self):
		"""clear the window and redraw the deck"""
		#pyglet.clock.tick()
		#self.window.switch_to()
		#self.window.dispatch_events()
		#self.window.dispatch_event('on_draw')
		#self.window.flip()
		pass

def debugtuio(path,args,types,src):
	"""print the arguments to the /tuio/2dcur message"""
	print args

def main():
	def tuio(dt):
		"""pyglet callback event to check for OSC messages"""
		server.recv(0.0333333333333)
	twoDcur=canvas()
	server = liblo.Server(3333)
	server.add_method('/tuio/2Dcur', None, twoDcur.handleOsc)
	#server.add_method('/tuio/2Dcur', None, debugtuio)
	while True:
		tuio(0)


if __name__ == "__main__":
	main()



