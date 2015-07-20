import sys,os
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3
from panda3d.bullet import *
from panda3d.core import BitMask32
from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
from panda3d.bullet import BulletDebugNode
import random

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
		self.box = loader.loadModel("skybox/earth_2")
		self.box.setScale(800) #was 300
		self.box.reparentTo(render)
		self.box.setLightOff()
		self.box.clearFog()
		self.lastUpdate=0
		
		#~ self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
		#~ self.debugNP.show()
		#~ self.world.setDebugNode(self.debugNP.node())
		
		self.accept('f1', self.toggleWireframe)
		self.accept('f2', self.toggleTexture)
		self.accept('f3', self.toggleDebug)
		self.accept('o',self.generate)
		
		ambientLight = AmbientLight('ambientLight')
		ambientLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
		ambientLightNP = render.attachNewNode(ambientLight)
		render.setLight(ambientLightNP)

		# Directional light 01
		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		# This light is facing backwards, towards the camera.
		directionalLightNP.setHpr(180, -20, 0)
		render.setLight(directionalLightNP)

		# Directional light 02
		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(Vec4(0.5, 0.6, 0.5, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		
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
		self.bodyNP.hide()
		
		#~ visNP = loader.loadModel('tumbleweed_1.egg')
		#~ geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		
		#~ shape=BulletConvexHullShape()
		#~ shape.addGeom(geom)
		#~ body = BulletRigidBodyNode('ast')
		#~ self.bodyNPAst = self.worldNP.attachNewNode(body)
		#~ self.bodyNPAst.node().addShape(shape)
		#~ self.bodyNPAst.node().setMass(1000.0)
		#~ self.bodyNPAst.setPos(0,400,0)
		#~ self.bodyNPAst.setCollideMask(BitMask32.allOn())
		#~ self.world.attachRigidBody(self.bodyNPAst.node())

		#~ visNP.reparentTo(self.bodyNPAst)


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

	def generate(self):
		astt=['Splargh','TehShoe','asteroid1','asteroid2']
		for i in range (75):
			
			posX=random.randint(-5000,5000)
			posY=random.randint(-5000,5000)
			posZ=random.randint(-5000,5000)
			nbAt = random.randint(1,50)
			for j in range (nbAt):
				choice=random.randint(0,3)
				visNP = loader.loadModel('models/' + str(astt[choice]) + '.bam')
				geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
				
				shape=BulletConvexHullShape()
				shape.addGeom(geom)
				body = BulletRigidBodyNode('ast')
				bodyNPAst = self.worldNP.attachNewNode(body)
				bodyNPAst.node().addShape(shape)
				bodyNPAst.node().setMass(1000.0)
				posX2=posX+random.randint(-200,200)
				posY2=posY+random.randint(-200,200)
				posZ2=posZ+random.randint(-200,200)
				bodyNPAst.setPos(posX2,posY2,posZ2)
				#~ h=random.uniform(-1,1)
				#~ p = random.uniform(-1,1) 
				#~ r = random.uniform(-1,1) 
				h = random.randint(-90,90)
				p = random.randint(-90,90)
				r = random.randint(-90,90)
				#~ print (h,p,r)
				bodyNPAst.setHpr(h,p,r)
				bodyNPAst.setCollideMask(BitMask32.allOn())
				self.world.attachRigidBody(bodyNPAst.node())
				bodyNPAst.setShaderAuto()

				visNP.reparentTo(bodyNPAst)
			
		print "done"

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
		#~ dt = globalClock.getRealTime() - self.lastUpdate
		
		dt = globalClock.getDt()
		force = Vec3(0, 0, 0)
		self.pyr={'p':0,'y':0,'r':0,'a':0,'w':0}
		self.speed=0
		if inputState.isSet('speedup'):
			
			self.speed+=300
		if inputState.isSet('speeddown'):
			self.speed-=300
			
		
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
		base.camera.setQuat(self.bodyNP.getQuat())
		base.camera.setPos(self.bodyNP.getPos())
			#~ print base.camera.getPos()
			#~ print base.camera.getHpr()
			#~ av=self.bodyNP.node().getAngularVelocity()
			
			#~ av2=av*0.5
			#~ self.bodyNP.node().setAngularVelocity(av2)
			#~ forwardVec=self.bodyNP.getQuat().getForward()
			
			#~ self.bodyNP.node().applyCentralForce(Vec3(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed))
			#~ self.bodyNP.node().applyTorque(Vec3(self.pyr['y']*300,0.0,self.pyr['p']*300))
			#~ self.bodyNP.node().setLinearVelocity((self.bodyNP.node().getLinearVelocity().getX()*0.98,self.bodyNP.node().getLinearVelocity().getY()*0.98,self.bodyNP.node().getLinearVelocity().getZ()*0.98))
			#~ print dt
		#~ if dt >0.02:
		self.lastUpdate=globalClock.getRealTime()
		self.world.doPhysics(dt)
		return task.cont
		
app=bulletTest()
run()