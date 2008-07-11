import simplejson, flickrapi, liblo, pyglet, math, rabbyt
from urllib import urlopen


class skreenPics:
	"""class to hold the pictures from flickr"""
	api_key = '59725ca9f32547bd79f608c18a2b7669'
	flickr = flickrapi.FlickrAPI(api_key)
	def jsonPstrip(self,str):
		"""strip jsonP style function call wrappers"""
		return str[str.find('(')+1:str.rfind(')')]
	def flickrRequest(self,func, **args):
		"""return simplejson parsed object of results"""
		return simplejson.loads(self.jsonPstrip(func(format='json',**args)))
	def __init__(self):
		"""do all the magic, and populate the sprites varable"""
		photos=self.flickrRequest(self.flickr.photos_search,tags="ir")['photos']['photo']
		urls=["http://farm%(farm)s.static.flickr.com/%(server)s/%(id)s_%(secret)s.jpg" % x for x in photos]
		images=[pyglet.image.load('a.jpg',urlopen(x)) for x in urls[0:10]]
		self.sprites=[rabbyt.Sprite(texture=x.texture) for x in images]
		[[sprite._set_scale(0.5)] for sprite in self.sprites]



class photoDeck(list):
	"""a stack of photos"""
	def draw(self):
		"""draw all of the photos, in stack order"""
		rabbyt.clear()
		rabbyt.render_unsorted(self)
	def pull(self,photo):
		"""put the last touched photo on top"""
		if photo != None:
			self.remove(photo)
			self.append(photo)
	def touchedPhoto(self,coord):
		"""return the touched photo at coordinates"""
		x,y=coord
		for photo in self.__reversed__():
			#~ if self.debug: print photo.x, photo.y, photo.left, photo.right, photo.top, photo.bottom
			if (photo.left < x) and (x < photo.right) and (photo.bottom < y) and (y < photo.top):
				return photo
		return None



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
	flipX=True
	flipY=True
	flipXDirection=True
	flipYDirection=True
	#TuioSimulator
	#~ flipX=False
	#~ flipY=True
	#~ flipXDirection=False
	#~ flipYDirection=True
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
		self.fingerUpdate()
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
		self.fingerRemove(finger)



class fingerTracker(touchStats):
	"""process the state of the fingers on the screen"""
	fingerPhoto=[]
	canvasFingers=[]
	def determineSelected(self):
		"""bind fingers to pictures, or the canvas"""
		if self.start:
			lD=self.latest[0]
			finger=self.latest
			xy=self.latest[1],self.latest[2]
			realxy=self.convert(*xy)
			photo=self.deck.touchedPhoto(realxy)
			if photo==None:
				self.canvasFingers.append(finger) 
			else:
				self.fingerPhoto.append((finger,photo))
		self.photoFingerList=[x[0][0] for x in self.fingerPhoto]
		self.canvasFingerList=[x[0] for x in self.canvasFingers]
	def fingerRemove(self,finger):
		"""remove a finger"""
		ID=finger[0]
		#~ if self.debug: print "fingerRemove"
		for finger,photo in self.fingerPhoto:
			if finger[0]==ID:
				self.fingerPhoto.remove((finger,photo))
		for finger in self.canvasFingers:
			if finger[0]==ID:
				self.canvasFingers.remove(finger)
		self.canvasFingerList=[x[0] for x in self.canvasFingers]
		self.removeFingerCounts(finger)
	def fingerUpdate(self):
		"""callback to update finger states"""
		self.determineSelected()
		#~ if self.debug: print "fP",self.fingerPhoto
		#~ if self.debug: print "CF",self.canvasFingers
		self.countFingers()

class fingerCounter(fingerTracker):
	movePhotos=[]
	rotatePhotos=[]
	scalePhotos=[]
	moveCanvas=(0,0)
	previousCenter=[]
	previousAngle=[]
	previousSpread=[]
	thisPhoto=None
	thisCenterPoint=(0,0)
	thisAngle=0
	thisSpread=0
	angleDiff=0
	spreadDiff=0
	GRAD_PI=180.0 / math.pi
	def getAngleTrig(self,point):
		"""find the angle from the origin of a point, from touchlib"""
		x,y=point
                if x==0:
                        if y < 0:
                                return 270
                        else:
                                return 90
                elif y ==0:
                        if x < 0:
                                return 180
                        else:
                                return 0
		if y > 0:
			if x > 0:
				return math.atan(y/x) * self.GRAD_PI
			else:
				return 180.0 - math.atan(y/-x) * self.GRAD_PI
		else:
			if x > 0:
				return 360.0 - math.atan(-y/x) * self.GRAD_PI
			else:
				return 180.0 + math.atan(-y/-x) * self.GRAD_PI
	def photoFingerCount(self):
		ID=self.latest[0]
		self.fingercount=[]
		if ID in self.photoFingerList:
			for finger,photo in self.fingerPhoto:
				if finger[0]==ID:
					self.thisPhoto=photo
					break
			for finger,photo in self.fingerPhoto:
				if photo==self.thisPhoto:
					for touches in self:
						if finger[0]==touches[0]:
							self.fingercount.append(touches)
		else:
			for canvasfinger in self.canvasFingers:
				for finger in self:
					if canvasfinger[0]==finger[0]:
						self.fingercount.append(finger)
	def findCenterPoint(self):
		points=[]
		for finger in self.fingercount:
			points.append((finger[1],finger[2]))
		avgX=sum([x for x,y in points]) / len(points)
		avgY=sum([y for x,y in points]) / len(points)
		self.thisCenterPoint=(avgX,avgY)
	def findAngle(self):
		fc=self.fingercount
		normalPoint=(fc[0][1]-fc[1][1],fc[0][2]-fc[1][2])
		self.thisAngle=self.getAngleTrig(normalPoint)
		print "angle", self.thisAngle, normalPoint
	def findAngleDiff(self):
		for entry in self.previousAngle:
			for finger in entry[0]:
				if self.latest[0] == finger[0]:
					self.angleDiff=entry[1]-self.thisAngle
					break
	def findSpread(self):
		fc=self.fingercount
		self.thisSpread=(float(fc[0][1])-float(fc[1][1]))**2 + (float(fc[0][2])-float(fc[1][2]))**2
	def findSpreadDiff(self):
		for entry in self.previousSpread:
			for finger in entry[0]:
				if self.latest[0] == finger[0]:
					self.spreadDiff=float(self.thisSpread-entry[1]) / float(entry[1])
					break
	def singleFingers(self):
		if not self.start:
			if len(self.fingercount) == 1:
				for diff in self.differences:
					if diff[0] == self.latest[0]:
						for finger, photo in self.fingerPhoto:
							if finger[0]==self.latest[0]:
								self.movePhotos.append((photo,diff[1],diff[2]))
	def twoFingers(self):
		if len(self.fingercount) == 2:
			self.findCenterPoint()
			self.findAngle()
			self.findSpread()
			self.processTwo()
	def removeFingerCounts(self,latest):
		for entry in self.previousAngle:
			for finger in entry[0]:
				if latest[0] == finger[0]:
					self.previousAngle.remove(entry)
		for entry in self.previousSpread:
			for finger in entry[0]:
				if latest[0] == finger[0]:
					self.previousSpread.remove(entry)
	def processTwo(self):
		self.findAngleDiff()
		self.findSpreadDiff()
		self.removeFingerCounts(self.latest)
		self.previousAngle.append((self.fingercount,self.thisAngle))
		self.previousSpread.append((self.fingercount,self.thisSpread))
		self.queueTwo()
	def queueTwo(self):
		self.rotatePhotos.append((self.thisPhoto,self.angleDiff))
		self.scalePhotos.append((self.thisPhoto,self.spreadDiff))
		print "rotate", self.rotatePhotos
		print "scale", self.scalePhotos
		thisRot=self.rotatePhotos[0]
		thisScale=self.scalePhotos[0]
		thisRot[0].rot+=thisRot[1]
		thisScale[0].scale+=thisScale[1]
	def multipleFingers(self):
		if len(self.fingercount) > 2:
			self.findCenterPoint()
			self.processMultiple()
	def processMultiple(self):
		pass
	def countFingers(self):
		#diffFingers=[x[0] for x in self.differences]
		#if self.latest[0] in diffFingers:
		self.movePhotos=[]
		self.rotatePhotos=[]
		self.scalePhotos=[]
		self.thisPhoto=None
		self.photoFingerCount()
		self.singleFingers()
		self.twoFingers()
		self.multipleFingers()
		self.takeAction()

	
class fingerActions(fingerCounter):
	"""perform actions based on the calculated stats of actions"""
	def rotatePictures(self):
		pass
	def moveCanvas(self):
		"""move the canvas based on differences of canvas bound fingers"""
		#~ if self.debug: print "moveCanvas"
		cDx,cDy = 0,0
		if self.latest[0] in self.canvasFingerList:
			diff=self.lastDiff
			cDx,cDy = (cDx + diff[1]) / 2 , (cDy + diff[2]) / 2
			cDx,cDy = self.convertChange(cDx,cDy)
			photoList=[x[1] for x in self.fingerPhoto]
			for photo in self.deck:
				if photo not in photoList:
					photo.x += cDx
					photo.y += cDy
	def redraw(self):
		"""clear the window and redraw the deck"""
		self.deck.draw()
	def movePictures(self):
		"""move pictures based on finger stats"""
		#~ if self.debug: print "movePictures"
		if self.latest[0] in self.photoFingerList:
			for finger,photo in self.fingerPhoto:
				if finger[0]==self.latest[0]:
					dx,dy=0,0
					latest,diff=self.latest,self.lastDiff
					if latest[0]==diff[0]:
						dx,dy = (dx+diff[1]) , (dy+diff[2])
					dx,dy = self.convertChange(dx,dy)
					photo.x+=dx
					photo.y+=dy
					self.deck.pull(photo)
					break
	def takeAction(self):
		"""callback to take action and then to redraw"""
		self.movePictures()
		self.rotatePictures()
		self.moveCanvas()
		self.redraw()

				


class canvas(fingerActions):
	"""main window"""
	window=pyglet.window.Window(fullscreen=True)
	#window=pyglet.window.Window(width=1024,height=768)
	#window=pyglet.window.Window()
	#~ debug = False
	def __init__(self,deck):
		self.deck=deck
		fingerActions.__init__(self)
	def redraw(self):
		"""clear the window and redraw the deck"""
		self.deck.draw()
	def pullLast(self):
		"""pull the last touched photo"""
		self.deck.pull(self.latestTouched)
	#window=pyglet.window.Window()

def debugtuio(path,args,types,src):
	"""print the arguments to the /tuio/2dcur message"""
	print args

def main():
	def tuio(dt):
		"""pyglet callback event to check for OSC messages"""
		server.recv(0.0333333333333)
	skreen=canvas(photoDeck(skreenPics().sprites))
	server = liblo.Server(3333)
	server.add_method('/tuio/2Dcur', None, skreen.handleOsc)
	#server.add_method('/tuio/2Dcur', None, debugtuio)
	pyglet.clock.schedule_interval(tuio, 0.0001)
	pyglet.clock.schedule(rabbyt.add_time)
	rabbyt.set_default_attribs()
	rabbyt.set_viewport((skreen.window.height,skreen.window.width))
	pyglet.app.run()


if __name__ == "__main__":
	main()
