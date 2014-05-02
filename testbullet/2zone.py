import xml.dom.minidom
import os, sys
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3
from panda3d.bullet import *
from pandac.PandaModules import *
from panda3d.core import BitMask32
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
		base.camera.setPos(0,-300,50)
		alight = AmbientLight('alight')
		alight.setColor(VBase4(0.8, 0.8, 0.9, 1))
		alnp = render.attachNewNode(alight)
		render.setLight(alnp)
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
		
		#~ self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
		#~ self.debugNP.show()
		#~ self.debugNP.node().showWireframe(True)
		#~ self.debugNP.node().showConstraints(True)
		#~ self.debugNP.node().showBoundingBoxes(False)
		#~ self.debugNP.node().showNormals(True)
		#~ self.world.setDebugNode(self.debugNP.node())
		
		#~ debugNode = BulletDebugNode('Debug')
		#~ debugNode.setVerbose(False)
		#~ debugNP = render.attachNewNode(debugNode)
		#~ debugNP.show()
		
		visNP = loader.loadModel('fighter.egg')
		visNP.ls()
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		#~ geomNodeCollection = visNP.findAllMatches('**/+GeomNode')
		#~ mesh = BulletTriangleMesh()
		#~ mesh.addGeom(geom)
		#~ for nodePath in geomNodeCollection: 
			#~ geomNode = nodePath.node() 
			#~ for i in range(geomNode.getNumGeoms()): 
				 #~ geom = geomNode.getGeom(i) 
				 #~ mesh.addGeom(geom) 
		#~ shape = BulletTriangleMeshShape(mesh, dynamic=True)
		shape=BulletConvexHullShape()
		shape.addGeom(geom)

		body = BulletRigidBodyNode('fighter')
		self.bodyNP = self.worldNP.attachNewNode(body)
		self.bodyNP.node().addShape(shape)
		self.bodyNP.node().setMass(1.0)
		self.bodyNP.setPos(-300, -300, -300)
		self.bodyNP.setCollideMask(BitMask32.allOn())
		#~ self.bodyNP.node().setCcdMotionThreshold(1e-7);
		#~ self.bodyNP.node().setCcdSweptSphereRadius(0.50);
		self.world.attachRigidBody(self.bodyNP.node())

		visNP.reparentTo(self.bodyNP)
		
		
		visNP = loader.loadModel('Splargh.egg')
		visNP.ls()
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		#~ mesh = BulletTriangleMesh()
		#~ geomNodeCollection = visNP.findAllMatches('**/+GeomNode')
		#~ mesh.addGeom(geom)
		#~ geom= BulletHelper.makeGeomFromLinks(visNP)
		
		#~ for nodePath in geomNodeCollection: 
			#~ geomNode = nodePath.node() 
			#~ for i in range(geomNode.getNumGeoms()): 
				 #~ geom = geomNode.getGeom(i) 
				 #~ mesh.addGeom(geom) 
		#~ mesh.addGeom(geom)
		#~ shape = BulletTriangleMeshShape(mesh, dynamic=True)
		shape=BulletConvexHullShape()
		shape.addGeom(geom)
		body = BulletRigidBodyNode('ast')
		self.bodyNPAst = self.worldNP.attachNewNode(body)
		self.bodyNPAst.node().addShape(shape)
		self.bodyNPAst.node().setMass(1000.0)
		self.bodyNPAst.setPos(0,400,0)
		#~ self.bodyNPAst.setPos(0, 0, 0)
		self.bodyNPAst.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(self.bodyNPAst.node())

		visNP.reparentTo(self.bodyNPAst)


		self.accept('escape', self.doExit)
		inputState.watchWithModifiers('up', 'z')
		inputState.watchWithModifiers('left', 'q')
		inputState.watchWithModifiers('down', 's')
		inputState.watchWithModifiers('right', 'd')
		inputState.watchWithModifiers('speedup', 'a')
		inputState.watchWithModifiers('speeddown', 'w')
		inputState.watchWithModifiers('reset', 'r')
		
		#~ self.loadZoneXml()
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
			
	def loadZoneXml(self):
		dom = xml.dom.minidom.parse("zone22.xml")
		items=dom.getElementsByTagName('item')
		for item in items:
			name=item.getElementsByTagName('name')[0].firstChild.data
			print name
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
				#~ tempAst=asteroid(iditem,(posx,posy,posz),(h,p,r),name,scale,self.id)
				#~ tempAst.setName(name)
				#~ self.listOfAsteroid.append(tempAst)
			visNP = loader.loadModel(egg)
			geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
			pt1, pt2 = visNP.getTightBounds() 
			xDim = pt2.getX() - pt1.getX() 
			yDim = pt2.getY() - pt1.getY()
			zDim = pt2.getZ() - pt1.getZ()
			#~ shape = BulletBoxShape(Vec3(xDim,yDim, zDim))
			shape=BulletConvexHullShape()
			shape.addGeom(geom)
			body = BulletRigidBodyNode(name)
			self.bodyNPAst = self.worldNP.attachNewNode(body)
			self.bodyNPAst.node().addShape(shape)
			self.bodyNPAst.node().setMass(1.0)
			self.bodyNPAst.setPos((posx,posy,posz))
			self.bodyNPAst.setHpr((h,p,r))
			self.bodyNPAst.setCollideMask(BitMask32.allOn())
			self.world.attachRigidBody(self.bodyNPAst.node())

			visNP.reparentTo(self.bodyNPAst)
			break

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
			self.speed+=200
		if inputState.isSet('speeddown'):
			self.speed-=200
		if inputState.isSet('left'):
			self.pyr['p']=1
		if inputState.isSet('up'):
			self.pyr['y']=-int(1)
		if inputState.isSet('down'):
			self.pyr['y']=int(1)
		if inputState.isSet('right'):
			self.pyr['p']=-1
		if inputState.isSet('reset'):
			self.bodyNP.setPos(0,0,0)
		#~ print self.pyr
		self.bodyNP.node().setActive(True)		
		#~ self.bodyNP.node().applyTorque  (Vec3(self.pyr['y']*300,0.0,self.pyr['p']*300))
		
		
		forwardVec=self.bodyNP.getQuat().getForward()
		#~ self.bodyNP.node().applyForce(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))
		self.bodyNP.node().applyCentralForce(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))
		v=Vec3(self.pyr['y']*300,0.0,self.pyr['p']*300)
		v= self.worldNP.getRelativeVector(self.bodyNP,v) 
		self.bodyNP.node().applyTorque(v)
		#~ self.bodyNP.node().applyTorque(Vec3(self.pyr['y']*300,0.0,self.pyr['p']*300))
		self.bodyNP.node().setLinearVelocity((self.bodyNP.node().getLinearVelocity().getX()*0.98,self.bodyNP.node().getLinearVelocity().getY()*0.98,self.bodyNP.node().getLinearVelocity().getZ()*0.98))
		self.world.doPhysics(dt)
		#~ print self.bodyNP
		#~ print self.bodyNP.getPos()
		ccou = (((forwardVec*(-200.0)) + self.bodyNP.getPos()) * 0.20) + (base.camera.getPos() * 0.80)
		pogi = self.bodyNP.getHpr()*0.1 + base.camera.getHpr()*0.9
		base.camera.setPos(ccou)
		base.camera.setHpr(pogi)
		
		av=self.bodyNP.node().getAngularVelocity()
		#~ print av
		av2=av*0.5
		self.bodyNP.node().setAngularVelocity(av2)
		return task.cont
		
app=bulletTest()
run()