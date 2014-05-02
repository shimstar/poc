import sys,os
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3
from panda3d.bullet import *
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
		self.torque=400
		self.box = loader.loadModel("skybox/earth")
		self.box.setScale(600) #was 300
		self.box.reparentTo(render)
		self.box.setLightOff()
		self.box.clearFog()
		
		self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
		self.debugNP.show()
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
		self.bodyNP.setPos(0, 0, 0)
		self.bodyNP.setCollideMask(BitMask32.allOn())
		#~ self.bodyNP.node().setCcdMotionThreshold(1e-7);
		#~ self.bodyNP.node().setCcdSweptSphereRadius(0.50);
		self.world.attachRigidBody(self.bodyNP.node())

		visNP.reparentTo(self.bodyNP)
		
		
		visNP = loader.loadModel('tumbleweed_1.egg')
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

	def toggleWireframe(self):
		base.toggleWireframe()

	def toggleTexture(self):
		base.toggleTexture()

	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()

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
			
			self.speed+=5
		if inputState.isSet('speeddown'):
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
		v=Vec3(self.pyr['y']*self.torque,0.0,self.pyr['p']*self.torque)
		v= self.worldNP.getRelativeVector(self.bodyNP,v) 
		self.bodyNP.node().applyTorque(v)
		
		self.bodyNP.node().applyCentralForce(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))

		self.bodyNP.node().setLinearVelocity((self.bodyNP.node().getLinearVelocity().getX()*0.98,self.bodyNP.node().getLinearVelocity().getY()*0.98,self.bodyNP.node().getLinearVelocity().getZ()*0.98))
		self.bodyNP.node().setAngularVelocity((self.bodyNP.node().getAngularVelocity().getX()*0.9,self.bodyNP.node().getAngularVelocity().getY()*0.9,self.bodyNP.node().getAngularVelocity().getZ()*0.9))
		
		#~ av=self.bodyNP.node().getAngularVelocity()
		
		#~ av2=av*0.5
		#~ self.bodyNP.node().setAngularVelocity(av2)
		#~ forwardVec=self.bodyNP.getQuat().getForward()
		
		#~ self.bodyNP.node().applyCentralForce(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))
		#~ self.bodyNP.node().applyTorque(Vec3(self.pyr['y']*300,0.0,self.pyr['p']*300))
		#~ self.bodyNP.node().setLinearVelocity((self.bodyNP.node().getLinearVelocity().getX()*0.98,self.bodyNP.node().getLinearVelocity().getY()*0.98,self.bodyNP.node().getLinearVelocity().getZ()*0.98))
		self.world.doPhysics(dt)
		return task.cont
		
app=bulletTest()
run()