#~ from pandac.PandaModules import loadPrcFileData 
#~ loadPrcFileData("", "threading-model Cull/Draw")
import xml.dom.minidom
import os, sys
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3
from panda3d.bullet import *
from panda3d.core import BitMask32
from panda3d.core import NodePath
from direct.showbase.InputStateGlobal import inputState
from panda3d.bullet import BulletDebugNode

class bulletTest(DirectObject):
	def __init__(self):
		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, 0))
		self.worldNP = render.attachNewNode('World')
		base.disableMouse()
		base.setFrameRateMeter(True)
		taskMgr.add(self.update, "update")
		base.camera.setPos(0,-100,250)
		self.obstacle=None
		
		self.box = loader.loadModel("skybox/earth")
		self.box.setScale(600) #was 300
		self.box.reparentTo(render)
		self.box.setLightOff()
		self.box.clearFog()
		
		self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
		self.debugNP.hide()
		self.world.setDebugNode(self.debugNP.node())
		
		self.accept('f1', self.toggleWireframe)
		self.accept('f2', self.toggleTexture)
		self.accept('f3', self.toggleDebug)
		self.accept('space', self.fire)
		self.bullet=[]

		
		visNP = loader.loadModel('fighter.egg')
		visNP2 = loader.loadModel('fighter.egg')
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
		
		self.loadZoneXml()
		base.disableMouse()
		base.camera.setPos(0,-300,50)
		

	def toggleWireframe(self):
		base.toggleWireframe()

	def toggleTexture(self):
		base.toggleTexture()

	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()
			
	def fire(self):
		self.speed=1000
		print "here"
		#~ world,worldNP=shimCollider.getInstance(weapon.zone).getWorld()
		visNP = loader.loadModel("sphere")
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)			
		shape=BulletConvexHullShape()
		shape.addGeom(geom)
		body = BulletRigidBodyNode("bullet")
		bodyNP = self.worldNP.attachNewNode(body)
		bodyNP.node().addShape(shape)
		bodyNP.node().setMass(0.0001)
		#~ bodyNP.setPos(self.bodyNP.getPos())
		bodyNP.setQuat(self.bodyNP.getQuat())
		bodyNP.setPos(self.bodyNP,Vec3(0,100,0))
		#~ bodyNP.setPos((0,100,0))
		bodyNP.setCollideMask(BitMask32.allOn())
		#~ bodyNP.setPythonTag("obj",self)
		self.world.attachRigidBody(bodyNP.node())
		visNP.reparentTo(bodyNP)
		forwardVec=bodyNP.getQuat().getForward()
		bodyNP.node().setLinearVelocity(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))
		self.bullet.append(body)
	
		
			
	def loadZoneXml(self):
		j=0
		dom = xml.dom.minidom.parse("zone2.xml")
		items=dom.getElementsByTagName('item')
		for item in items:
			if j<50:
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

				self.bodyNPAst.setPos((posx,posy,posz))
				self.bodyNPAst.setHpr((h,p,r))
				self.bodyNPAst.setCollideMask(BitMask32.allOn())
				self.world.attachRigidBody(self.bodyNPAst.node())

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
		self.speed=0
		if inputState.isSet('speedup'):
			self.speed+=400
		if inputState.isSet('speeddown'):
			self.speed-=400
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

		
		
		forwardVec=self.bodyNP.getQuat().getForward()
		
		f=Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed)
		#~ print "#########"
		#~ print f
		f= self.worldNP.getRelativeVector(self.bodyNP,f) 
		#~ print f
		self.bodyNP.node().applyCentralForce(f)
		#~ self.bodyNP.node().applyCentralForce(Vec3(100,0,0))
		v=Vec3(self.pyr['y']*500,0.0,self.pyr['p']*500)
		v= self.worldNP.getRelativeVector(self.bodyNP,v) 
		self.bodyNP.node().applyTorque(v)
		
		self.bodyNP.node().setLinearVelocity((self.bodyNP.node().getLinearVelocity().getX()*0.98,self.bodyNP.node().getLinearVelocity().getY()*0.98,self.bodyNP.node().getLinearVelocity().getZ()*0.98))
		self.world.doPhysics(dt)

		mvtCam = (((forwardVec*(-200.0)) + self.bodyNP.getPos()) * 0.20) + (base.camera.getPos() * 0.80)
		hprCam = self.bodyNP.getHpr()*0.1 + base.camera.getHpr()*0.9
		base.camera.setPos(mvtCam)
		base.camera.setHpr(hprCam)
		
		av=self.bodyNP.node().getAngularVelocity()
		#~ print av
		av2=av*0.8
		self.bodyNP.node().setAngularVelocity(av2)
		
	
		#~ print self.bodyNP.getQuat()
		#~ print self.bodyNP.getHpr()
		
		#~ print "###########"
		for b in self.bullet:
			result = self.world.contactTest(b)
			for contact in result.getContacts():
				print contact.getNode0()
				print contact.getNode1()
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