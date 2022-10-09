#Jessica Ortiz 20192
#sr5 texturas

from cargar import *

from textures import Texture

#tamaño de lienzo
render = Render(1000, 1000)

#cargar textura
texture = Texture('textureF.bmp')


#descmentarear solo el blque de codigo que se quiera renderizar

#medium
#               eye, center, up
# render.lookAt(V3(-0.2,0,20), V3(0,0,0), V3(0,1,0))
# render.glObjModel('formica.obj',translate=(0,0,0), scale=(0.3,0.3,0.3), rotate=(0,-1.5,0), texture=texture)

# #imagen final
# render.glFinish('Medium.bmp')


#Low
#               eye, center, up
# render.lookAt(V3(0.1,-1,20), V3(0,0,0), V3(0,1,0))
# render.glObjModel('formica.obj',translate=(0,0,0), scale=(0.3,0.3,0.3), rotate=(-0.5,-1.5,0), texture=texture)

# #imagen final
# render.glFinish('Low.bmp')



#High
#               eye, center, up
# render.lookAt(V3(0.1,1,20), V3(0,0,0), V3(0,1,0))
# render.glObjModel('formica.obj',translate=(0,0,0), scale=(0.3,0.3,0.3), rotate=(0.5,-1.5,0), texture=texture)

# #imagen final
# render.glFinish('High.bmp')


#Dutch
#               eye, center, up
render.lookAt(V3(-0.5,0,20), V3(0,0,0), V3(0,1,0))
render.glObjModel('formica.obj',translate=(0,0,0), scale=(0.3,0.3,0.3), rotate=(0.5,-2,0), texture=texture)

#imagen final
render.glFinish('Dutch.bmp')