from pandac.PandaModules import loadPrcFileData 
loadPrcFileData("model-cache-dir",".\cache")
loadPrcFileData("model-cache-textures", "1" )
import sys,os
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import Point3,Vec3,Vec4
from panda3d.bullet import *
stepSize = 1.0 / 60.0
ang_step=0.3
stepTorque=150
class odeTest(DirectObject):
	def __init__(self):
		self.world = BulletWorld()
		self.world.setGravity(Vec3(0, 0, -9.81))
		#~ self.world = OdeWorld()
		#~ self.world.setGravity(0, 0, 0)
		#~ self.world.initSurfaceTable(1)
		#~ self.world.setSurfaceEntry(0, 0, 0.8, 0.1, 10, 0.8, 0.00005, 0, 1)
		#~ self.space = OdeSimpleSpace()
		#~ self.space = OdeHashSpace() 
		#~ self.space.setLevels(-3,6) 
		self.space.setAutoCollideWorld(self.world)
		self.contactgroup = OdeJointGroup() 
		self.space.setAutoCollideJointGroup(self.contactgroup)
		self.space.setCollisionEvent("yourCollision")
		self.shipModel= loader.loadModel("fighter")
		self.shipModel.reparentTo(render)
		self.asteroid=loader.loadModel("tumbleweed")
		self.asteroid.setScale(30)
		self.asteroid.reparentTo(render)
		self.astBody,self.astGeom=self.createOdeBody(self.asteroid,5000)
		self.odeBody,self.odeGeom=self.createOdeBody(self.shipModel,10)
		self.odeBody.setPosition(0,0,0)
		self.astBody.setPosition(0,200,0)
		self.odeBody.setQuaternion(Quat(self.shipModel.getQuat()))
		self.astBody.setQuaternion(Quat(self.asteroid.getQuat()))
		self.space.setSurfaceType(self.astGeom, 0)
		#~ print self.astBody.getQuaternion()
		#~ print self.odeBody.getQuaternion()
		self.box = loader.loadModel("skybox/earth")
		self.box.setScale(600) #was 300
		self.box.reparentTo(render)
		self.box.setLightOff()
		self.box.clearFog()
		self.keysDown={'toto':'titi'}
		self.keysDown.clear()
		self.accept("z",self.keyDown,['z',1])
		self.accept("z-up",self.keyDown,['z',0])
		self.accept("q",self.keyDown,['q',1])
		self.accept("q-up",self.keyDown,['q',0])
		self.accept("s",self.keyDown,['s',1])
		self.accept("s-up",self.keyDown,['s',0])
		self.accept("d",self.keyDown,['d',1])
		self.accept("d-up",self.keyDown,['d',0])
		self.accept("a",self.keyDown,['a',1])
		self.accept("a-up",self.keyDown,['a',0])
		self.accept("w",self.keyDown,['w',1])
		self.accept("w-up",self.keyDown,['w',0])
		self.accept("w",self.keyDown,['x',1])
		self.accept("w-up",self.keyDown,['x',0])
		self.accept('yourCollision',self.onCollision)
		self.last=0
		self.currentTorqueX=0
		self.currentTorqueZ=0
		self.speed=0
		base.disableMouse()
		base.setFrameRateMeter(True)
		taskMgr.add(self.controlCamera, "camera-task")
		base.camera.setPos(0,-300,50)
		self.angVelX=0
		self.angVelY=0
	
	def onCollision(self,entry):
		self.speed=0
	
	def createOdeBody(self,obj,mass,radius=1.01):
		pt1, pt2 = obj.getTightBounds() 
		xDim = pt2.getX() - pt1.getX() 
		yDim = pt2.getY() - pt1.getY() 
		zDim = pt2.getZ() - pt1.getZ() 
		odeBody = OdeBody(self.world) 
		odeMass = OdeMass()
		odeMass.setBoxTotal(mass, xDim, yDim, zDim)
		
		odeBody.setMass( odeMass ) 
		boxGeom = OdeBoxGeom(self.space, xDim, yDim, zDim)
		boxGeom.setCollideBits(BitMask32(0x00000001))
		boxGeom.setCategoryBits(BitMask32(0x00000001))
		boxGeom.setBody(odeBody)
		
		return odeBody,boxGeom
		
	def controlCamera(self, task):
		
		dt = task.time - self.last  #obtains the time since that last frame.
		self.last = task.time
		
		self.shipModel.setPos( self.odeBody.getPosition() ) 
		self.shipModel.setQuat( Quat(self.odeBody.getQuaternion()) ) 
		
		if dt > stepSize:
			cc=self.space.autoCollide()
			self.world.quickStep(dt)	
			self.contactgroup.empty()
			quat=Quat(self.odeBody.getQuaternion())
			if self.keysDown.has_key('q'):
				if self.keysDown['q']!=0:
					self.angVelY-=ang_step
					self.shipModel.setHpr(self.shipModel, 1,0,0)
					pass
			if self.keysDown.has_key('d'):
				if (self.keysDown['d']!=0):
					self.angVelY+=ang_step
					self.shipModel.setHpr(self.shipModel, -1,0,0)
					pass
			if self.keysDown.has_key('z'):
				if (self.keysDown['z']!=0):
					self.shipModel.setHpr(self.shipModel, 0,-1,0)
					self.angVelX-=ang_step
			if self.keysDown.has_key('s'):
				if (self.keysDown['s']!=0):
					self.angVelX+=ang_step
					self.shipModel.setHpr(self.shipModel, 0,1,0)
			if self.keysDown.has_key('a'):
				if (self.keysDown['a']!=0):
					self.speed+=10
					
			if self.keysDown.has_key('w'):
				if (self.keysDown['w']!=0):
					self.speed-=10
					
			self.odeBody.setQuaternion(self.shipModel.getQuat())
			forwardVec=Quat(self.odeBody.getQuaternion()).getForward()
			self.odeBody.setLinearVel(forwardVec.getX()*self.speed,forwardVec.getY()*self.speed,forwardVec.getZ()*self.speed)
			forwardVec.normalize
			ccou = (((forwardVec*(-200.0)) + self.odeBody.getPosition()) * 0.20) + (base.camera.getPos() * 0.80)
			pogi = Quat(self.odeBody.getQuaternion()).getHpr()*0.1 + base.camera.getHpr()*0.9
			base.camera.setPos(ccou)
			base.camera.setHpr(pogi)


			av=self.odeBody.getAngularVel()
			av2=av*0.5
			self.odeBody.setAngularVel(av2)

			self.shipModel.setPos( self.odeBody.getPosition() ) 
			self.shipModel.setQuat( Quat(self.odeBody.getQuaternion()) ) 

			self.asteroid.setPos(self.astBody.getPosition())
			self.asteroid.setQuat(Quat(self.astBody.getQuaternion()))
		#~ base.camera.lookAt(self.shipModel)

		return Task.cont
		
	def keyDown(self,key,value):
		if value==0:
			if self.keysDown.has_key(key)==1:
				del self.keysDown[key]
		else:
			self.keysDown[key]=value
		
		
app=odeTest()
run()