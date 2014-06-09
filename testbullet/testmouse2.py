#~ from pandac.PandaModules import loadPrcFileData 
#~ loadPrcFileData("", "threading-model Cull/Draw")
import xml.dom.minidom
import os, sys
import math
from pandac.PandaModules import CollisionTraverser,CollisionNode
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3,Quat
from panda3d.bullet import *
from panda3d.core import *
from panda3d.core import NodePath
from direct.showbase.InputStateGlobal import inputState
from panda3d.bullet import BulletDebugNode

class bulletTest(DirectObject):
	def __init__(self):
		self.listOfAsteroid={}
		self.windowSizeX = base.win.getXSize()
		self.windowSizeY = base.win.getYSize()
		self.centerX = self.windowSizeX / 2
		self.centerY = self.windowSizeY / 2
		self.factor=float(self.windowSizeX)/float(self.windowSizeY)
		print self.factor
		print str(self.windowSizeX) + "/" + str(self.windowSizeY)
		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, 0))
		self.worldNP = render.attachNewNode('World')
		base.disableMouse()
		base.setFrameRateMeter(True)
		taskMgr.add(self.update, "update")
		base.camera.setPos(0,-100,250)
		self.obstacle=None
		self.speed=0
		self.torque=1200
		self.box = loader.loadModel("skybox/earth")
		self.box.setScale(600) #was 300
		self.box.reparentTo(render)
		self.box.setLightOff()
		self.box.clearFog()
		self.mousebtn = [0,0,0]
		self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
		self.debugNP.hide()
		self.world.setDebugNode(self.debugNP.node())
		self.picker = CollisionTraverser()            #Make a traverser
		base.cTrav  = CollisionTraverser()
		self.hdlCollider=CollisionHandlerEvent()
		self.hdlCollider.addInPattern('into-%in')
		self.hdlCollider.addOutPattern('outof-%in')
		self.pickerNode=CollisionNode('mouseRay')
		self.pickerNP=base.camera.attachNewNode(self.pickerNode)
		self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
		self.pickerRay=CollisionRay()
		self.pq     = CollisionHandlerQueue()         #Make a handler
		self.pickerNode.addSolid(self.pickerRay)
		self.picker.addCollider(self.pickerNP, self.pq)
		taskMgr.add(self.pickmouse,"pickmouse")
		self.pointToLookAt=Vec3(0,0,0)
		self.accept('f1', self.toggleWireframe)
		self.accept('f2', self.toggleTexture)
		self.accept('f3', self.toggleDebug)
		self.accept('space', self.fire)
		self.accept("mouse1", self.setMouseBtn, [0, 1])
		self.accept("mouse1-up", self.setMouseBtn, [0, 0])
		self.accept("mouse2", self.setMouseBtn, [1, 1])
		self.accept("mouse2-up", self.setMouseBtn, [1, 0])
		self.accept("mouse3", self.setMouseBtn, [2, 1])
		self.accept("mouse3-up", self.setMouseBtn, [2, 0])
		self.accept("wheel_up", self.speedUp,[5])
		self.accept("wheel_down", self.speedUp,[-5])
		#~ self.accept("wheel_down",self.wheelDown)
		self.bullet=[]

		
		#~ visNP = loader.loadModel('fighter.egg')
		#~ visNP2 = loader.loadModel('fighter.egg')
		visNP = loader.loadModel('dark2.egg')
		visNP2 = loader.loadModel('dark2.egg')
		#~ text = loader.loadTexture("dark_fighter_6_color.png")
		#~ visNP.setTexture(text)
		#~ visNP.ls()
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		shape=BulletConvexHullShape()
		shape.addGeom(geom)

		
		body = BulletRigidBodyNode('fighter')
		self.bodyNP = self.worldNP.attachNewNode(body)
		self.bodyNP.node().addShape(shape)
		self.bodyNP.node().setMass(1.0)
		self.bodyNP.setPos(0, 0, 0)
		self.bodyNP.setCollideMask(BitMask32.allOn())

		self.world.attachRigidBody(self.bodyNP.node())

		visNP.reparentTo(self.bodyNP)
		
		#~ body2 = BulletGhostNode('ghost')
		#~ self.bodyNP2=self.worldNP.attachNewNode(body2)
		#~ shape2=BulletConvexHullShape()
		#~ geom = visNP2.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		#~ shape2.addGeom(geom)
		#~ self.bodyNP2.node().addShape(shape2)
		#~ visNP2.reparentTo(self.bodyNP2)
		#~ self.bodyNP2.setPos(0, 100, 0)

		#~ self.bodyNP2.setCollideMask(BitMask32(0x0f))
		#~ self.world.attachGhost(self.bodyNP2.node())
		#~ self.bodyNP2.reparentTo(self.bodyNP)
		
		visNP = loader.loadModel('Substation/model_1.egg')
		visNP.ls()
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)

		shape=BulletConvexHullShape()
		shape.addGeom(geom)

		body = BulletRigidBodyNode('station')
		self.bodyNPst = self.worldNP.attachNewNode(body)
		self.bodyNPst.node().addShape(shape)
		
		self.bodyNPst.setPos(0, 31800, 0)
		self.bodyNPst.setCollideMask(BitMask32.allOn())
		self.bodyNPst.setTag("name","station")
		self.world.attachRigidBody(self.bodyNPst.node())

		visNP.reparentTo(self.bodyNPst)

		self.accept('escape', self.doExit)
		inputState.watchWithModifiers('up', 'z')
		inputState.watchWithModifiers('left', 'q')
		inputState.watchWithModifiers('down', 's')
		inputState.watchWithModifiers('right', 'd')
		inputState.watchWithModifiers('speedup', 'a')
		inputState.watchWithModifiers('speeddown', 'w')
		self.pointerToGo = loader.loadModelCopy("arrow")
		self.pointerToGo.reparentTo(render)
		self.pointerToGo.hide()
		self.loadZoneXml()
		base.disableMouse()
		base.camera.setPos(0,-300,50)
		
	def speedUp(self,sp):
		
		self.speed+=sp
		if self.speed<0:
			self.speed=0
		elif self.speed>100:
			self.speed=100
		
	def pickmouse(self,task):
		mpos=base.mouseWatcherNode.getMouse()
		self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

		self.picker.traverse(render)
		if self.pq.getNumEntries() > 0:
			self.pq.sortEntries() #this is so we get the closest object
			nodeInQueue=self.pq.getEntry(0).getIntoNodePath()
			#~ print self.pq.getEntry(0).getInteriorPoint(nodeInQueue)
			#~ print nodeInQueue.getPos()
			#~ print nodeInQueue
			
				#~ print index
				#~ print str(nodeInQueue)[index:index+6]
			print nodeInQueue.getTag("id")
			print nodeInQueue.getTag("name")
			self.pointToLookAt=None
			if str(nodeInQueue).find('earth')==-1:
				if str(nodeInQueue).find("Ast_")>0:
					index= str(nodeInQueue).find("Ast_")
					ast=str(nodeInQueue)[index:index+6]
					self.pointToLookAt=self.listOfAsteroid[ast].getPos()
					#~ print self.pointToLookAt
			
		return task.cont
		
		
	def toggleWireframe(self):
		base.toggleWireframe()

	def setMouseBtn(self, btn, value):
		self.mousebtn[btn]=value

	def toggleTexture(self):
		base.toggleTexture()

	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()
			
	def fire(self):
		#~ mpos = base.mouseWatcherNode.getMouse()
		#~ self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
 
		#~ base.cTrav.traverse(render)
		#~ if myHandler.getNumEntries() > 0:
				#~ self.collHandler.sortEntries()
		visNP = loader.loadModel("sphere.bam")
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)			
		shape=BulletConvexHullShape()
		shape.addGeom(geom)
		body = BulletRigidBodyNode("bullet")
		bodyNP = self.worldNP.attachNewNode(body)
		bodyNP.node().addShape(shape)
		bodyNP.node().setMass(0.0001)
		bodyNP.setPos(self.bodyNP,Vec3(0,100,0))
		#~ x=base.mouseWatcherNode.getMouseX()
		#~ y=base.mouseWatcherNode.getMouseY()
		md = base.win.getPointer(0)
		#~ x = md.getX()
		#~ y = md.getY()
		x=base.mouseWatcherNode.getMouseX()
		y=base.mouseWatcherNode.getMouseY()
		h=self.bodyNP.getH()
		p=self.bodyNP.getP()
		i=self.bodyNP.getQuat().getI()
		j=self.bodyNP.getQuat().getJ()
		k=self.bodyNP.getQuat().getK()
		r=self.bodyNP.getQuat().getR()
		
		pp=LVector3f()
		#~ lens = PerspectiveLens()
		#~ lens.setFilmSize(20, 15)
		#~ base.camLens.setNearFar(10, 5000)
		t1=Point3()
		t2=Point3()
		#~ ret=base.camLens.extrudeVec(Point2(x,y),pp)
		
		
		#    ~ print ret
		#~ print "pp =  " + str(pp)
		#~ print t1
		#~ print t2
		if self.pointToLookAt!=None:
			bodyNP.lookAt(self.pointToLookAt)
		else:
			ret=base.camLens.extrude(Point2(x,y),t1,t2)
			t2=t2/100
			t2relative=render.getRelativePoint(camera,t2)   	
			bodyNP.lookAt(t2relative)
		#~ self.pointerToGo.setPos(self.bodyNP.getPos())
		#~ self.pointerToGo.lookAt(self.pointToLookAt)
		#~ bodyNP.setQuat(self.pointerToGo.getQuat())
		#~ bodyNP.setQuat(self.bodyNP.getQuat())
		#~ ang=180*math.atan2(x,y)/3.14
		#~ print ang
		
		#~ bodyNP.setH(bodyNP,x*ang*-1)
		#~ bodyNP.setP(bodyNP,y*ang)
		#~ h = h + (x - self.centerX) 
		#~ p = p + (y - self.centerY) 
		#~ if (p < -45): p = -45
		#~ if (p >  45): p =  45
		print (x,y)
		print (h,p)
		#~ negX=-1
		#~ if h<0:
			#~ negX=1
		#~ negY=1
		#~ if h<0:
			#~ negY=- 1
		
		#~ x=55*+x*negX
		#~ y=55*y*negY
		#~ print(r,i,j,k)
		#~ print self.bodyNP.getQuat()
		#~ bodyNP.setHpr(h+30*self.factor*x,p+30*y,0)
		#~ bodyNP.setHpr(h+x,p+y,0)
		
		#~ i=i+30*x
		#~ j=j+30*y
		
		#~ bodyNP.setQuat(Quat(r,i,j,k))
		print bodyNP.getHpr()
		print self.bodyNP.getHpr()
		#~ print bodyNP.getQuat()
		print "######################"
		
		bodyNP.setCollideMask(BitMask32.allOn())
		#~ bodyNP.setPythonTag("obj",self)
		self.world.attachRigidBody(bodyNP.node())
		visNP.reparentTo(bodyNP)
		forwardVec=bodyNP.getQuat().getForward()
		bodyNP.node().setLinearVelocity(Vec3(forwardVec.getX()*1000,forwardVec.getY()*1000,forwardVec.getZ()*1000))
		self.bullet.append(body)
	
		
			
	def loadZoneXml(self):
		j=0
		dom = xml.dom.minidom.parse("zone2.xml")
		items=dom.getElementsByTagName('item')
		for item in items:
			if j<100:
				name=item.getElementsByTagName('name')[0].firstChild.data
				typitem=item.getElementsByTagName('type')[0].firstChild.data
				egg=item.getElementsByTagName('eggast')[0].firstChild.data
				pos=item.getElementsByTagName('pos')[0].firstChild.data
				tabPos=pos.split(",")
				posx=float(tabPos[0])
				posy=float(tabPos[1])
				posz=float(tabPos[2])
				h,p,r=0,0,0
				if item.getElementsByTagName('hpr')!=None:
					if len(item.getElementsByTagName('hpr'))>0:
						hpr=item.getElementsByTagName('hpr')[0].firstChild.data
						tabHpr=hpr.split(",")
						h=float(tabHpr[0])
						p=float(tabHpr[1])
						r=float(tabHpr[2])

				visNP = loader.loadModel(egg)
				geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)

				shape=BulletConvexHullShape()
				shape.addGeom(geom)
				

				body = BulletRigidBodyNode(name)
				self.bodyNPAst = self.worldNP.attachNewNode(body)
				self.bodyNPAst.node().addShape(shape)
				self.bodyNPAst.setTag("name","ast")
				self.bodyNPAst.node().setTag("id",str(j))

				self.bodyNPAst.setPos((posx,posy,posz))
				self.bodyNPAst.setHpr((h,p,r))
				self.bodyNPAst.setCollideMask(BitMask32.allOn())
				self.world.attachRigidBody(self.bodyNPAst.node())
				self.listOfAsteroid[name]=self.bodyNPAst
				visNP.reparentTo(self.bodyNPAst)
			j+=1

	def doExit(self):
		self.cleanup()
		sys.exit(1)

	def cleanup(self):
		self.world = None
		self.worldNP.removeNode()

	def update(self,task):
		dt = globalClock.getDt()
		force = Vec3(0, 0, 0)
		self.pyr={'p':0,'y':0,'r':0,'a':0,'w':0}
		x=0
		y=0
		if base.mouseWatcherNode.hasMouse():
			x=-base.mouseWatcherNode.getMouseX()
			y=base.mouseWatcherNode.getMouseY()
			absx=abs(x)
			absy=abs(y)
			if absx>0.25 and absx<0.5:
				x*=2
			elif absx>=0.5 and absx<0.75:
				x*=4
			elif absx>=0.75:
				x*=6
			if absy>0.25 and absy<0.5:
				y*=2
			elif absy>=0.5 and absy<0.75:
				y*=4
			elif absy>=0.75:
				y*=6
				
				
		
		if inputState.isSet('speedup'):
			if self.speed<100:
				self.speed+=5
		if inputState.isSet('speeddown'):
			if self.speed>0:
				self.speed-=5
			
		if inputState.isSet('left'):
			self.pyr['p']=1
		if inputState.isSet('up'):
			self.pyr['y']=-int(1)
		if inputState.isSet('down'):
			self.pyr['y']=int(1)
		if inputState.isSet('right'):
			self.pyr['p']=-1
		#~ print self.pyr
		self.bodyNP.node().setActive(True)		
		#~ self.bodyNP.node().applyTorque  (Vec3(self.pyr['y']*300,0.0,self.pyr['p']*300))
		forwardVec=self.bodyNP.getQuat().getForward()
		if self.mousebtn[2]==1:
			v=Vec3(y*self.torque,0.0,x*self.torque)
			v= self.worldNP.getRelativeVector(self.bodyNP,v) 
			self.bodyNP.node().applyTorque(v)
		
		self.bodyNP.node().applyCentralForce(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))

		self.bodyNP.node().setLinearVelocity((self.bodyNP.node().getLinearVelocity().getX()*0.98,self.bodyNP.node().getLinearVelocity().getY()*0.98,self.bodyNP.node().getLinearVelocity().getZ()*0.98))
		#~ self.bodyNP.node().setAngularVelocity((self.bodyNP.node().getAngularVelocity().getX()*0.9,self.bodyNP.node().getAngularVelocity().getY()*0.9,self.bodyNP.node().getAngularVelocity().getZ()*0.9))
		
		self.world.doPhysics(dt)

		mvtCam = (((forwardVec*(-200.0)) + self.bodyNP.getPos()) * 0.30) + (base.camera.getPos() * 0.70)
		hprCam = self.bodyNP.getHpr()*0.9 + base.camera.getHpr()*0.1
		base.camera.setPos(mvtCam)
		base.camera.setHpr(hprCam)
		#~ base.camera.lookAt(base.mouse)
		
		av=self.bodyNP.node().getAngularVelocity()
		#~ print av
		av2=av*0.72
		self.bodyNP.node().setAngularVelocity(av2)
		
	
		#~ print self.bodyNP.getQuat()
		#~ print self.bodyNP.getHpr()
		
		#~ print "###########"
		#~ for b in self.bullet:
			#~ result = self.world.contactTest(b)
			#~ for contact in result.getContacts():
				#~ print contact.getNode0()
				#~ print contact.getNode1()
		#~ ghost = self.bodyNP2.node()
		
		#~ for node in result.getContacts():
		#~ for node in ghost.getOverlappingNodes():
			#~ if self.obstacle!= node:
				#~ print node.getNode0()
				#~ print node.getNode1()
				#~ print node.getShapes()
				#~ self.obstacle= node
				#~ nodenode=NodePath(node)
				#~ if node.getTag("name")!="station":
				#~ pt1, pt2 = nodenode.getTightBounds() 
				#~ xDim = pt2.getX() - pt1.getX() 
				#~ yDim = pt2.getY() - pt1.getY() 
				#~ zDim = pt2.getZ() - pt1.getZ() 
				
				#~ dimMax=xDim
				#~ if  yDim>dimMax:
					#~ dimMax=yDim
				#~ if zDim>dimMax:
					#~ dimMax=zDim
					
				#~ print dimMax
				
				#~ visNP = loader.loadModel('fighter.egg')
				#~ visNP.setPos(nodenode.getPos())
				#~ visNP.setPos(nodenode,(dimMax*1.5,0,0))
				#~ visNP.reparentTo(render)
			#~ print contact.getNode0()
			#~ print contact.getNode1()
			#~ mpoint = contact.getManifoldPoint()
			#~ print mpoint
		
		return task.cont
		
app=bulletTest()
run()