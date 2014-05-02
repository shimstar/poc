from pandac.PandaModules import loadPrcFileData 
loadPrcFileData('', 'win-size %i %i' % (1280, 720))
from panda3d.rocket import *
from direct.directbase import DirectStart


LoadFontFace("assets/brassiere.ttf")

r = RocketRegion.make('pandaRocket', base.win)
r.setActive(1)
context = r.getContext()

doc = context.LoadDocument('windows/infoshipgame.rml')
#~ doc.AddEventListener("click","test2()")
doc.Show()
#~ doc = context.LoadDocument('data/menudialogue.rml')
#~ doc.Show()
#~ ti=doc.GetElementById("title")
#~ print ti

#~ co=doc.GetElementById("contentHero")
#~ i=0
#~ div=doc.CreateElement("div")
#~ div.SetAttribute("width","50px")
#~ div.SetAttribute("height","150px")
#~ div.SetAttribute("id","id1")
#~ div.SetAttribute("style","position:absolute;top:100px;left:" + str((50+i*150)) + "px;z-index:" + str(2) + ";width:150px;")

#~ el=doc.CreateElement('img')
#~ el.SetAttribute("src","../images/face1.png")

#~ div.AddEventListener("click","test('ERERER')")
#~ div.AppendChild(el)
#~ co.AppendChild(div)
#~ i=1
#~ div=doc.CreateElement("div")
#~ div.SetAttribute("id","id2")
#~ div.SetAttribute("width","50px")
#~ div.SetAttribute("height","150px")
#~ div.SetAttribute("style","position:absolute;top:100px;left:" + str((50+i*150)) + "px;z-index:" + str(3) + ";width:150px;")
#~ el=doc.CreateElement('img')
#~ el.SetAttribute("src","../images/face2.png")

#~ div.AddEventListener("click","test('ERERER2')")
#~ div.AppendChild(el)
#~ co.AppendChild(div)


doc.Show()

ih = RocketInputHandler()
base.mouseWatcher.attachNewNode(ih)
r.setInputHandler(ih)

run()
