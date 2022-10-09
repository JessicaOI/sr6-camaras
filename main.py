#Jessica Ortiz 20192
#sr5 texturas

from cargar import Render

from textures import Texture

#tamaño de lienzo
render = Render(1000, 1000)

#cargar textura
texture = Texture('textureF.bmp')

#definicr objeto, posicion(xyz), tamaño, textura
render.glObjModel('formica.obj', (5, 0, 0), (100, 100, 100), texture=texture)

#imagen final
render.glFinish('output.bmp')