#Jessica Ortiz 20192
#sr5 texturas

from cargar import *

from textures import Texture

#tamaño de lienzo
render = Render(1000, 1000)

#cargar textura
texture = Texture('textureF.bmp')

render.lookAt(V3(-0.2,0,20), V3(0,0,0), V3(0,1,0))
render.glObjModel('formica.obj',translate=(0,0,0), scale=(0.3,0.3,0.3), rotate=(0,0.5,0.36), texture=texture)

#imagen final
render.glFinish('output.bmp')