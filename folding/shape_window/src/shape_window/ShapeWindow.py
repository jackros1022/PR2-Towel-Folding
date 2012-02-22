import roslib; roslib.load_manifest('shape_window')
from shape_window import Geometry2D 
import cv
import sys
import thread
import time
import math
from shape_window import ShapeWindowUtils

## The ShapeWindow is a simple HighGUI-based viewer which can keep track of shapes, as defined in the Geometry2D package. Used by the FoldingGUI
class ShapeWindow:
	def __init__(self,name="New Shape Window",size=(1500,1000)):
		print "Using this shapewindow"
		self.name = name
		self.size = size
		cv.NamedWindow(name)
		cv.WaitKey(10)
		self.background = cv.CreateImage(size,8,3)
		self.img = cv.CreateImage(size,8,3)
		self.shapesLock = thread.allocate_lock()
		self.initMembers()
		
		self.closed = False
		self.update()
		self.setListeners()
		thread.start_new_thread(self.continually_update,())

	def initMembers(self):
		self.shapes = []
		self.temp = []
		self.overlay = []
		self.proposed = []
		self.selected = []
		self.last_mouseover = []
		self.last_mouseover_overlay = []
		self.snap_points = []
		self.snap_range = 5
		self.initBasic()
		self.initExtended()
	
	def initBasic(self):
		#Line Drawing Members
		self.startPt = Geometry2D.Point(0,0)
		self.endPt = Geometry2D.Point(0,0)
		#Poly Drawing Members
		self.newPoly = []
		self.drawColor = Colors.GREEN
		self.lineColor = Colors.WHITE
	
	def initExtended(self):
		return
	
	def continually_update(self):
		while(not self.isClosed()):
			if self.UPDATE_GRAPHICS:		
				self.update()
				time.sleep(0.01)
		cv.WaitKey(100)
		cv.DestroyWindow(self.name)
		for i in range(10):
			cv.WaitKey(1)
		return
		
	def close(self):
		self.closed = True
	
	def isClosed(self):
		return self.closed
		
	def update(self):
		self.shapesLock.acquire()
		#try:
		cv.Copy(self.background,self.img)
			#print "length of self.shapes %d , length of proposed: %d"%(len(self.getShapes()), len(self.proposed))
		for cvShape in sorted(self.getShapes(),key = lambda x: x.getHeight()):
			cvShape.drawToImage(self.img,'')
		for button in sorted(self.getOverlay(),key = lambda x: x.getHeight()):
			button.drawToImage(self.img,'')
		for cvShape in sorted(self.temp,key = lambda x: x.getHeight()):
			cvShape.drawToImage(self.img,'')
		for cvShape in sorted(self.proposed, key = lambda x: x.getHeight()):
			cvShape.drawToImage(self.img,'temp')
		for cvShape in sorted(self.selected, key = lambda x: x.getHeight()):
			cvShape.drawToImage(self.img, 'sel')
		cv.ShowImage(self.name,self.img)		
		self.shapesLock.release()		
		return cv.WaitKey(10)
		#
		#	print "Unexpected error:", sys.exc_info()[0], sys.exc_value
			#raise
		
	
	def clearTemp(self):
		self.shapesLock.acquire()
		for shape in self.temp:
			self.temp.remove(shape)
		self.shapesLock.release()

	def clearProposed(self):
		self.shapesLock.acquire()
		for shape in self.proposed:
			self.proposed.remove(shape)
		self.proposed = []
		self.shapesLock.release()

	def clearSelected(self):
		self.shapesLock.acquire()
		for shape in self.selected:
			self.selected.remove(shape)
		self.selected = []
		self.shapesLock.release()

	def addPropCVShape(self,cvShape):
		self.proposed.append(cvShape)

	def addSelectedCVShape(self, cvShape):
		self.selected.append(cvShape)
		
	def addCVShape(self, cvShape):
		self.shapes.append(cvShape)
		
	def addOverlay(self, button):
		self.overlay.append(button)
		
	def addTempCVShape(self, cvShape):
		self.temp.append(cvShape)
	
	def removeCVShape(self,shape):
		#self.shapesLock.acquire()
		self.shapes.remove(shape)
		#self.shapesLock.release()
	
	def removeTempCVShape(self,shape):
		self.temp.remove(shape)
	
	def removeOverlay(self,button):
		self.overlay.remove(button)
		
	def clearHeight(self,height):
		for shape in self.shapes:
			if shape.getHeight()==height:
				self.removeCVShape(shape)

	def clearShapes(self):
		self.shapesLock.acquire()
		self.shapes = []
		self.proposed = []
		self.selected = []
		self.shapesLock.release()
				
	def setListeners(self):
		cv.SetMouseCallback(self.name,self.handleEvents,0)
		
	def shapeListeners(self):
		return True
    
	def handleEvents(self,event,x,y,flags,param):
		self.clearTemp()
		#Check buttons first
		onButton = False
		for button in self.getOverlay():
			if button.getShape().contains(Geometry2D.Point(x,y)):
				onButton = True
				if not button in self.last_mouseover_overlay:
					self.last_mouseover_overlay.append(button)
					button.onMouseOn(event,x,y,flags,param)
				button.onMouse(event,x,y,flags,param)
			else:
				if button in self.last_mouseover_overlay:
					self.last_mouseover_overlay.remove(button)
					button.onMouseOff(event,x,y,flags,param)
		if onButton:
			return
		thread.start_new_thread(self.onMouseLocked,(event,x,y,flags,param))
		if(self.shapeListeners()):
			for cvShape in self.getShapes():
				if cvShape in self.getHighlighted(x,y):
					if not cvShape in self.last_mouseover:
						self.last_mouseover.append(cvShape)
						cvShape.onMouseOn(event,x,y,flags,param)
					cvShape.onMouse(event,x,y,flags,param)
				else:
					if cvShape in self.last_mouseover:
						self.last_mouseover.remove(cvShape)
						cvShape.onMouseOff(event,x,y,flags,param)
		return
		
	def getHighlighted(self,x,y):
		return [cvShape for cvShape in self.getShapes() if cvShape.getShape().contains(Geometry2D.Point(x,y))]
		
	def onMouseLocked(self,event,x,y,flags,param):
		self.shapesLock.acquire()
		self.onMouse(event,x,y,flags,param)
		self.shapesLock.release()
		
	def onMouse(self,event,x,y,flags,param):
		return self.lineDrawer(event,x,y,flags,param)
		
	def polyDrawer(self,event,x,y,flags,param):
		if event == cv.CV_EVENT_LBUTTONDOWN:
			print "Left button: Point x:%f, y:%f"%(x,y)
			self.newPoly.append(Geometry2D.Point(x,y))
			
		elif event == cv.CV_EVENT_RBUTTONDOWN:
			print "Right button"
			poly = Geometry2D.Polygon(*self.makeRectangle(self.newPoly[0]))
			#poly = Geometry2D.Polygon(*self.newPoly)
			print "Num polygon vertices", len(self.makeRectangle(self.newPoly[0]))
			cvPoly = CVPolygon(self.getDrawColor(),0,poly)
			self.addCVShape(cvPoly)
			self.newPoly = []	
			return True
		
		elif len(self.newPoly) > 1:
			startPt = self.newPoly[-1]
			print "StartPoint", startPt
			endPt = Geometry2D.Point(x,y)
			print "End Point"
			line = Geometry2D.LineSegment(startPt,endPt)
			cvLine = CVLineSegment(self.lineColor,self.tempFront(),line)
		 #self.addTempCVShape(cvLine)
		for i, pt in enumerate(self.newPoly):
			self.highlightPt(pt)
			if i > 0:
				startPt = self.newPoly[i-1]
				line = Geometry2D.LineSegment(startPt,pt)
				cvLine = CVLineSegment(self.lineColor,self.tempFront(),line)
				self.addTempCVShape(cvLine)
			elif i == len(self.newPoly)-1:
				endPt = self.newPoly[0]
				line = Geometry2D.LineSegment(pt,endPt)
				cvLine = CVLineSegment(self.lineColor,self.tempFront(), line)
				self.addTempCVShape(cvLine)
		return False

	def getDrawColor(self):
		return self.drawColor
	
	def setDrawColor(self,color):
		self.drawColor = color
	
	def lineDrawer(self,event,x,y,flags,param):
		if event == cv.CV_EVENT_LBUTTONDOWN:
			self.startPt = Geometry2D.Point(x,y)
		elif event == cv.CV_EVENT_LBUTTONUP:
			self.endPt = Geometry2D.Point(x,y)
			line = Geometry2D.DirectedLineSegment(self.startPt,self.endPt)
			self.addCVShape(CVDirectedLineSegment(cv.RGB(255,255,255),10,line,2))
		
		elif cv.CV_EVENT_FLAG_LBUTTON == flags-32:
			line = Geometry2D.DirectedLineSegment(self.startPt,Geometry2D.Point(x,y))
			self.addTempCVShape(CVDirectedLineSegment(cv.RGB(150,150,150),10,line,2))

		elif event == cv.CV_EVENT_RBUTTONDOWN:
			self.startPt = Geometry2D.Point(x,y)
		elif event == cv.CV_EVENT_RBUTTONUP:
			self.endPt = Geometry2D.Point(x,y)
			line = Geometry2D.DirectedLineSegment(self.startPt,self.endPt)
			self.addCVShape(CVDirectedLineSegment(cv.RGB(0,0,255),10,line,2))
		return
		
	def front(self):
		if len(self.getShapes()) == 0:
			return 0
		return max([shape.getHeight() for shape in self.shapes])+1
	
	def front(self, polys):
		if len(polys) == 0:
			return 0
		return max([shape.getHeight() for shape in polys])+1
		
	def tempFront(self):
		if len(self.getTempShapes()) == 0:
			return 0
		return max([shape.getHeight() for shape in self.getTempShapes()])+1
	
	def back(self):
		if len(self.getShapes()) == 0:
			return 0
		return min([shape.getHeight() for shape in self.shapes])-1
	
	def tempBack(self):
		if len(self.getTempShapes()) == 0:
			return 0
		return min([shape.getHeight() for shape in self.getTempShapes()])-1
		
	def getShapes(self):
		return self.shapes

	def getShapesCopy(self):
		return [shape.dupl() for shape in self.getShapes()]

	def getOverlay(self):
		return self.overlay

	def getPolys(self):
		return [cvShape for cvShape in self.shapes if cvShape.getShape().isPolygon()]

	def getPolysCopy(self):
		return [cvShape.dupl() for cvShape in self.shapes if cvShape.getShape().isPolygon()]
	
	def getTempShapes(self):
		return self.temp
		
	def highlightPt(self,pt):
		return self.addPropCVShape(CVCircle(Colors.WHITE,self.tempFront(),Geometry2D.Circle(pt,3)))
		
	def highlightSegment(self,seg):
		return self.addTempCVShape(CVLineSegment(Colors.GREY,self.tempFront(),seg))
		
	def highlightPoly(self,poly):
		return self.addTempCVShape(CVPolygon(Colors.BLUE,self.tempFront(),poly))
		
	def snapToAllLines(self,pt):
		lines = ShapeWindowUtils.flatten([poly.getShape().sides() for poly in self.getShapes() if poly.getShape().isPolygon()])
		return self.snapToLines(pt,lines)
		
	def snapToLines(self,pt,lines):
		if len(lines) == 0:
			return pt
		snapLine = min([Geometry2D.ptSegmentDisplacement(pt,line) for line in lines],key = lambda displ: displ.length())
		return snapLine.end()
		
	def isCovered(self,pt,cvShape, polys):
		for shape in [cvPoly.getShape() for cvPoly in polys if cvPoly.getHeight() >= cvShape.getHeight() and not cvPoly == cvShape]:
			if shape.contains(pt):
				#print "Found covered vertex %s"%pt
				return True
		return False
		
	def getSize(self):
		return self.size
		
	def snapPoints(self):
		return self.snap_points
		
	def addSnapPoint(self,pt):
		self.snap_points.append(pt)
		
	def removeSnapPoint(self,pt):
		self.snap_points.remove(pt)
	
	def clearSnapPoints(self):
		self.snap_points = []
		
	def setSnapRange(self,val):
		self.snap_range = val
	
	def getSnapRange(self):
		return self.snap_range
		
	def snapToPoint(self,x,y):
		clickPt = Geometry2D.Point(x,y)
		min_distance = self.getSnapRange()
		for snapPt in self.snapPoints():
			if Geometry2D.distance(clickPt,snapPt) <= min_distance:
				return (snapPt.x(),snapPt.y())
		return (x,y)	
		
	def setOnMouse(self,fxn):
		self.onMouse = fxn

    	

class CVShape:
	
	def __init__(self,color,height,shape,*params):
		self.color = color
		self.height = height
		self.shape = shape
		self.highlighted = False
		self.params = params
		self.foldLine = None
		self.hang = False
		self.hangDirection  = False
		self.prevHang = False
	
	def getShape(self):
		return self.shape
	
	def drawToImage(self,img):
		abstract
		
	def getHeight(self):
		return self.height
		
	def setHeight(self,height):
		self.height = height
		
	def getColor(self):
		return self.color
		
	def getDrawColor(self):
		return self.getColor()
		
	def setColor(self,color):
		self.color = color
	
	def getParams(self):
		return self.params
	
	def setParams(self,*params):
		self.params = params

	def isHang(self):
		return self.hang;

	def setHang(self, isHang, direction='None'):
		self.hang = isHang;
		self.hangDirection = direction


	def getHangDirection(self):
		return self.hangDirection

	def setPrevHang(self,isPrevHang):
		self.prevHang = isPrevHang

	def isPrevHang(self):
		return self.prevHang

	def onMouse(self,event,x,y,flags,param):
		return
		
	def onMouseOn(self,event,x,y,flags,param):
		return
		
	def onMouseOff(self,event,x,y,flags,param):
		return
		
	def invertColor(self):
		(red, green, blue, alpha) = self.getColor()
		self.setColor(cv.RGB(255-red,255-green,255-blue))
	
	def getDarkColor(self):
		return Colors.darkenCV(self.getColor(),0.1)
		
	def getLightColor(self):
		return Colors.lightenCV(self.getColor(),0.1)
		
	def __str__(self):
		return "|Shape: %s\nColor: %s, Height:%d, Hang:%s|"%(self.shape,self.color,self.height,self.hang)

	def dupl(self):
		return self.__class__(self.getColor(),self.getHeight(),self.getShape(),self.getParams()) 
	
		
class CVLine(CVShape):

	def drawToImage(self,img,imgtype):
		#computer later..
		return 0
	
	def drawToImage(self,img):
		#compute later..
		return 0
		
	def thickness(self):
		params = self.getParams()
		if len(params) >= 1:
			return params[0]
		else:
			return 2

	def dupl(self):
		return CVLine(self.getColor(),self.getHeight(),self.getShape().dupl())

					    
class CVLineSegment(CVLine):
						    
	def drawToImage(self,img, imgtype=''):
		line = self.shape
		pt1 = line.start()
		pt2 = line.end()
		dx = 0
		dy = 0
		if imgtype == 'sel':
			dx = 1000
			dy = 0
		if imgtype == 'temp':
			dx = 500
			dy = 0
		pt1 = pt1.dupl()
		pt1.translate(dx,dy)
		pt2 = pt2.dupl()
		pt2.translate(dx,dy)	
		return cv.Line(img,pt1.toTuple(),pt2.toTuple(),self.getDrawColor(),self.thickness())

class CVDirectedLineSegment(CVLineSegment):
		
	def drawToImage(self,img, imgtype):
		return CVLineSegment.drawToImage(self,img,imgtype)
		

class CVPolygon(CVShape):
		
	def drawToImage(self,img,imgtype):
		pts = []
		if not (imgtype=='temp' or imgtype == 'sel'):
			pts = [pt.toTuple() for pt in self.getShape().vertices()]
			
		elif (imgtype == 'temp'):
			pts = [(int(pt.x() + 500),int(pt.y())) for pt in self.getShape().vertices()]
		else:
			pts = [(int(pt.x() + 1000),int(pt.y())) for pt in self.getShape().vertices()]
		cv.FillPoly(img,[pts],self.getDrawColor())
		for side in self.getShape().sides():
			pt1 = side.start()
			pt2 = side.end()
			dy = 0
			dx = 0
			if imgtype == 'temp':
				dx = 500
				dy = 0
			if imgtype == 'sel':
				dx = 1000
			        dy = 0
			
			pt1 = pt1.dupl()
			pt1.translate(dx,dy)
			pt2 = pt2.dupl()
			pt2.translate(dx,dy)
			
			cv.Line(img,pt1.toTuple(),pt2.toTuple(),cv.RGB(150,150,150),1)

	def dupl(self):
		newCV = CVPolygon(self.getColor(),self.getHeight(),self.getShape(),self.getParams())
		newCV.setHang(self.isHang(), self.getHangDirection());
		newCV.foldLine = self.foldLine
		return newCV

class CVCircle(CVShape):

	def filled(self):
		if len(self.getParams()) == 0:
			return True
		else:
			return self.getParams()[0]

	def drawToImage(self,img,imgtype):
		circle = self.shape
		center = circle.center()
		if (imgtype == 'temp'):
			center = Geometry2D.translatePt(center, 500,0)
		elif(imgtype == 'sel'):
			center = Geometry2D.translatePt(center, 1000,0)
		if self.filled():
			return cv.Circle(img, center.toTuple(),int(circle.radius()),self.getDrawColor(),-1)
		else:
			return cv.Circle(img,center.toTuple(),int(circle.radius()),self.getDrawColor(),1)


(DEFAULT,HIGHLIGHTED,PRESSED) = range(3)
class CVButton(CVPolygon):

	
	def __init__(self,text,bottomLeft,onClick,height=1,color=False):
		if not color:
			color = Colors.SILVER
		self.text = text
		self.font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX,0.75,0.75)
		self.bottomLeft = bottomLeft	
		self.onClick = onClick
		self.status = DEFAULT
		
		CVPolygon.__init__(self,color,height,None)
		
	def getShape(self):
		((buttonWidth,buttonHeight),baseline) = cv.GetTextSize(self.getText(),self.getFont())
		origin = self.getBottomLeft()
		xMin = origin.x()-4
		xMax = origin.x() + buttonWidth
		yMin = origin.y() - buttonHeight
		yMax = origin.y()+4
		return Geometry2D.Polygon(Geometry2D.Point(xMin,yMin),Geometry2D.Point(xMin,yMax),Geometry2D.Point(xMax,yMax),Geometry2D.Point(xMax,yMin))
       
	def getBottomLeft(self):
		return self.bottomLeft
	
	def setBottomLeft(self,pt):
		self.bottomLeft = pt
		
	def getFont(self):
		return self.font
	
	def setFont(self,font):
		self.font = font
		
	def getText(self):
		return self.text
	
	def setText(self,text):
		self.text = text
		
	def setOnClick(self,fxn):
		self.onClick = fxn
	
	def getOnClick(self):
		return self.onClick
		
	def getDrawColor(self):
		if self.status == DEFAULT:
			return self.getColor()
		elif self.status == HIGHLIGHTED:
			return Colors.lightenCV(self.getColor(),0.1)
		elif self.status == PRESSED:
			return Colors.darkenCV(self.getColor(),0.2)
		
	def onMouse(self,event,x,y,flags,param):
		if event == cv.CV_EVENT_LBUTTONDOWN:
			self.status = PRESSED
		elif event == cv.CV_EVENT_LBUTTONUP:
			self.getOnClick()()
			self.status = HIGHLIGHTED
		else:
			self.status = HIGHLIGHTED
	
	def onMouseOff(self,event,x,y,flags,param):
		self.status = DEFAULT
	
	def onMouseOn(self,event,x,y,flags,param):
		self.status = HIGHLIGHTED
	
	
	def getSize(self):
		((width,height),baseline) =  cv.GetTextSize(self.getText(),self.getFont())
		return (width+8,height + baseline+8)
	def drawToImage(self,img,imgtype):
		CVPolygon.drawToImage(self,img, imgtype)
		cv.PutText(img,self.getText(),self.getBottomLeft().toTuple(),self.getFont(),Colors.BLACK)

class CVLabel(CVPolygon):

	def __init__(self,text,bottomLeft,height=1,color=False):
                if not color:
                        color = Colors.SILVER
                self.text = text
                self.font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX,0.75,0.75)
                self.bottomLeft = bottomLeft

                CVPolygon.__init__(self,color,height,None)

        def getShape(self):
                ((buttonWidth,buttonHeight),baseline) = cv.GetTextSize(self.getText(),self.getFont())
                origin = self.getBottomLeft()
                xMin = origin.x()-4
                xMax = origin.x() + buttonWidth
                yMin = origin.y() - buttonHeight
                yMax = origin.y()+4
                return Geometry2D.Polygon(Geometry2D.Point(xMin,yMin),Geometry2D.Point(xMin,yMax),Geometry2D.Point(xMax,yMax),Geometry2D.Point(xMax,yMin))

        def getBottomLeft(self):
                return self.bottomLeft

        def setBottomLeft(self,pt):
                self.bottomLeft = pt

        def getFont(self):
                return self.font

        def setFont(self,font):
                self.font = font

        def getText(self):
                return self.text

        def setText(self,text):
                self.text = text

	def getSize(self):
                ((width,height),baseline) =  cv.GetTextSize(self.getText(),self.getFont())
                return (width+8,height + baseline+8)

	def drawToImage(self,img,imgtype):
		CVPolygon.drawToImage(self,img, imgtype)
		cv.PutText(img,self.getText(),self.getBottomLeft().toTuple(),self.getFont(),Colors.BLACK)



class CVOnOffButton(CVButton):
	def __init__(self,text,bottomLeft,valueGetter,valueToggle):
		self.valueGetter = valueGetter
		self.valueToggle = valueToggle
		CVButton.__init__(self,text=text,bottomLeft=bottomLeft,onClick=self.toggleOnOff)
	
	def isOn(self):
		if not self.valueGetter or not self.valueToggle:
			return self.onFlag
		else:
			return self.valueGetter()
	
	def toggleOnOff(self):
		if not self.valueGetter or not self.valueToggle:
			self.onFlag = not self.onFlag
		else:
			self.valueToggle()
	
	def getColor(self):
		if self.isOn():
			return Colors.GREEN
		else:
			return Colors.RED
		
	
class CVSlider(CVPolygon):
	
	def __init__(self,origin,valMin,valMax,valueGetter=False,valueSetter=False,sliderWidth=150,sliderHeight=25,caption="Slider"):
		self.origin = origin
		self.setRange(valMin,valMax)
		self.valueGetter = valueGetter
		self.valueSetter = valueSetter
		self.sliderWidth = float(sliderWidth)
		self.sliderHeight = float(sliderHeight)
		self.caption = caption
		CVShape.__init__(self,Colors.DARKGREY,1,None)
	
	def getShape(self):
		pt1 = self.getOrigin()
		pt2 = Geometry2D.Point(pt1.x(),pt1.y()-self.getSliderHeight())
		pt3 = Geometry2D.Point(pt2.x()+self.getSliderWidth(),pt2.y())
		pt4 = Geometry2D.Point(pt3.x(),pt1.y())
		return Geometry2D.Polygon(pt1,pt2,pt3,pt4)
		
	def getOrigin(self):
		return self.origin
	
	def setOrigin(self,pt):
		self.origin = pt
	
	def getSliderHeight(self):
		return self.sliderHeight
	
	def setSliderHeight(self,height):
		self.sliderHeight = height
	
	def getSliderWidth(self):
		return self.sliderWidth
	
	def setSliderWidth(self,width):
		self.sliderWidth = width
	
	def getRange(self):
		return (self.valMin,self.valMax)
	
	def setRange(self, valMin,valMax):
		self.valMin = float(valMin)
		self.valMax = float(valMax)
	
	def getCaption(self):
		return self.caption
	
	def setCaption(self, caption):
		self.caption = caption
		
	def getValue(self):
		if not self.valueGetter or not self.valueSetter:
			return self.value
		else:
			return self.valueGetter()
	
	def setValue(self,value):
		if not self.valueGetter or not self.valueSetter:
			self.value = value
		else:
			self.valueSetter(value)
	
		
	def getBar(self):
		(valMin,valMax) = self.getRange()
		value = self.getValue()
		pct = (value - valMin) / (valMax - valMin)
		origin = self.getOrigin()
		barWidth = 5.0
		pt1 = Geometry2D.Point(origin.x()-barWidth/2 + pct*self.getSliderWidth(), origin.y())
		pt2 = Geometry2D.Point(pt1.x(),pt1.y() - self.getSliderHeight())
		pt3 = Geometry2D.Point(pt1.x()+barWidth,pt2.y())
		pt4 = Geometry2D.Point(pt3.x(),pt1.y())
		bar = Geometry2D.Polygon(pt1,pt2,pt3,pt4)
		return CVPolygon(Colors.invertCV(self.getColor()),1,bar)
		
	def getLine(self):
		origin = self.getOrigin()
		pt1 = Geometry2D.Point(origin.x(),origin.y() - self.getSliderHeight()/2)
		pt2 = Geometry2D.Point(pt1.x() + self.getSliderWidth(), pt1.y())
		line = Geometry2D.LineSegment(pt1,pt2)
		return CVLineSegment(Colors.BLACK,1,line)
		
		
	def drawToImage(self,img,imgtype):
		CVPolygon.drawToImage(self,img,imgtype)
		self.getLine().drawToImage(img,imgtype)
		self.getBar().drawToImage(img,imgtype)
		
	def onMouse(self,event,x,y,flags,param):
		flags -= 32
		if flags == cv.CV_EVENT_FLAG_LBUTTON:
			origin = self.getOrigin()
			width = self.getSliderWidth()
			(valMin,valMax) = self.getRange()
			pct = (x - origin.x()) / width
			value = (1-pct)*valMin + pct*valMax
			self.setValue(value)
			
class CVVisualizer(CVCircle):
	def __init__(self,origin,valueGetter,color,displayCondition=lambda:True):
		self.valueGetter = valueGetter
		self.displayCondition = displayCondition
		circle = Geometry2D.Circle(origin,1)
		CVShape.__init__(self,color=color,height=1,shape=circle)
		
	def getValue(self):
		return self.valueGetter()
	
	def getOrigin(self):
		return self.origin
		
	def setOrigin(self,pt):
		self.origin = pt
		
	def drawToImage(self,img,imgtype):
		if self.displayCondition():
			self.getShape().setRadius(self.getValue())
			CVCircle.drawToImage(self,img,imgtype)
		
	
		
def shapeWindowPrint(text):
	print text
		
class Colors:
	
	RED = cv.RGB(255,0,0)
	GREEN = cv.RGB(0,255,0)
	BLUE = cv.RGB(0,0,255)
	YELLOW = cv.RGB(255,255,0)
	SKYBLUE = cv.RGB(0,255,255)
	PINK = cv.RGB(255,0,255)
	WHITE = cv.RGB(255,255,255)
	GREY = cv.RGB(150,150,150)
	DARKGREY = cv.RGB(50,50,50)
	SILVER = cv.RGB(200,200,200)
	BLACK = cv.RGB(0,0,0)
	
	
	@staticmethod
	def lightenCV(cvColor,percent):
		return Colors.RGBtoCV(Colors.lightenRGB(Colors.CVtoRGB(cvColor),percent))
	
	@staticmethod
	def lightenRGB(rgbColor,percent):
		return Colors.HSLtoRGB(Colors.lightenHSL(Colors.RGBtoHSL(rgbColor),percent))
	
	@staticmethod
	def lightenHSL(hslColor,percent):
		[H, S, L] = [float(c) for c in hslColor]
		L = min(1.0, L + percent)
		return (H,S,L)
	
	@staticmethod
	def darkenCV(cvColor,percent):
		return Colors.RGBtoCV(Colors.darkenRGB(Colors.CVtoRGB(cvColor),percent))
	
	@staticmethod
	def darkenRGB(rgbColor,percent):
		return Colors.HSLtoRGB(Colors.darkenHSL(Colors.RGBtoHSL(rgbColor),percent))
	
	@staticmethod
	def darkenHSL(hslColor,percent):
		[H, S, L] = [float(c) for c in hslColor]
		L = max(0, L - percent)
		return (H,S,L)
		
	@staticmethod
	def complementCV(cvColor):
		return Colors.RGBtoCV(Colors.complementRGB(Colors.CVtoRGB(cvColor)))
		
	@staticmethod
	def complementRGB(rgbColor):
		return Colors.HSLtoRGB(Colors.complementHSL(Colors.RGBtoHSL(rgbColor)))
		
	@staticmethod
	def complementHSL(hslColor):
		[H,S,L] = [float(c) for c in hslColor]
		H = (H + 180) % 360
		return (H,S,L)
		
	@staticmethod
	def invertCV(cvColor):
		return Colors.RGBtoCV(Colors.invertRGB(Colors.CVtoRGB(cvColor)))
		
	@staticmethod
	def invertRGB(rgbColor):
		[R,G,B] = [float(c) for c in rgbColor]
		return [(255-R),(255-G),(255-B)]
		
	@staticmethod
	def invertHSL(hslColor):
		return Colors.RGBtoHSL(Colors.invertRGB(Colors.HSLtoRGB(hslColor)))
		
	@staticmethod
	def RGBtoCV(rgbColor):
		return cv.RGB(*rgbColor)
		
	@staticmethod
	def CVtoRGB(cvColor):
		(B,G,R,A) = cvColor
		return (R,G,B)
	
	
	@staticmethod
	def RGBtoHSL(rgbColor):
		[R, G, B] = [float(c) for c in rgbColor]
		R /= 255
		G /= 255
		B /= 255
		maxColor = max([R,G,B])
		minColor = min([R,G,B])
		L = (maxColor + minColor) / 2
		if maxColor == minColor:
			S = 0
			H = 0
		else:
			if L < 0.5:
				S = (maxColor - minColor) / (maxColor + minColor)
			else:
				S = (maxColor - minColor) / (2 - maxColor - minColor)
			if R == maxColor:
				H = (G-B) / (maxColor - minColor)
			elif G == maxColor:
				H = 2.0 + (B-R)/(maxColor - minColor)
			else:
				H = 4.0 + (R-G) / (maxColor - minColor)
		H *= 60
		return (H,S,L)
	
	@staticmethod
	def HSLtoRGB(hslColor):
		[H, S, L] = [float(c) for c in hslColor]
		if S==0:
			R = G = B = L
		else:
			if L < 0.5:
				temp2 = L * (1.0 + S)
			else:
				temp2 = L + S - L*S
			temp1 = 2.0*L - temp2
			H /= 360
			temp3R = Colors.normTemp3(H + 1.0 / 3.0)
			temp3G  = Colors.normTemp3(H)
			temp3B = Colors.normTemp3(H - 1.0 / 3.0)
			R = Colors.getColorFromTemps(temp1,temp2,temp3R)
			G = Colors.getColorFromTemps(temp1,temp2,temp3G)
			B = Colors.getColorFromTemps(temp1,temp2,temp3B)
			
		R *= 255
		G *= 255
		B *= 255
		return (R,G,B)

	@staticmethod	
	def normTemp3(temp3):
		if temp3 < 0:
			return temp3 + 1
		elif temp3 > 1:
			return temp3 - 1
		else:
			return temp3
	
	@staticmethod	
	def getColorFromTemps(temp1,temp2,temp3):
		if 6.0*temp3 < 1:
			return temp1 + (temp2-temp1)*6.0*temp3
		elif 2.0*temp3 < 1:
			return temp2
		elif 3.0*temp3 < 2:
			return temp1 + (temp2-temp1)*((2.0/3.0)-temp3)*6.0
		else:
			return temp1
			  


