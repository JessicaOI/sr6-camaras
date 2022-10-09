#Jessica Ortiz 20192
#sr5 texturas

import struct

from obj import Obj

from matrixmath import theorem, multM

from collections import namedtuple

from math import sin, cos

V2 = namedtuple('Vertex2', ['x', 'y'])

V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(c):
    # 2 bytes
    return struct.pack('=h', c)

def dword(c):
    # 4 bytes 
    return struct.pack('=l', c)


def color(r, g, b):
    return bytes([b, g, r])


def barycentric(A, B, C, P):
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x), 
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary[2]) < 1:
        return -1, -1, -1  

    return (
        1 - (bary[0] + bary[1]) / bary[2], 
        bary[1] / bary[2], 
        bary[0] / bary[2]
    )

def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

#producto punto
def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

#producto cruz
def cross(v0, v1):
    return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
)

#bounding box
def bbox(*vertices): 
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]
    xs.sort()
    ys.sort()

    return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])


class Render(object):
 
  #Inicializan valores
  def __init__(self, width, height):
        self.current_color = color(1, 1, 1)
        self.clear_color = color(0,0,0)
        self.active_texture = None

        self.glCreateWindow(width, height)
  
  # Se crea el margen con el cual se va a trabajar
  def glCreateWindow(self, width, height):
      self.width = width
      self.height = height
      self.glClear()
      self.glViewport(0,0, width, height)

  def glViewport(self, x, y, width, height):
    self.vpX = x
    self.vpY = y
    self.vpWidth = width
    self.vpHeight = height

  # Se definen colores con los cuales trabajar
  def glClear(self):
      self.framebuffer = [
      [self.clear_color for x in range(self.width)] 
      for y in range(self.height)
      ]
      self.zbuffer = [
        [-float('inf') for x in range(self.width)]
        for y in range(self.height)
      ]
      self.zClear = [
        [self.clear_color for x in range(self.width)]
        for y in range(self.height)
      ]

  def glClearColor(self, r, g, b):
        self.clearColor = color(r * 255, b*255, g*255)
        self.glClear()

  #Da el color al punto creado en pantalla 
  def glPoint(self, x, y, color = None):
      if x >= self.width or x < 0 or y >= self.height or y < 0:
          return
      try:
          self.framebuffer[y][x] = color or self.current_color
      except:
          pass

  #Gnerar vertex
  def glVertex(self, x, y, color = None):
      pixelX = ( x + 1) * (self.vpWidth  / 2 ) + self.vpX
      pixelY = ( y + 1) * (self.vpHeight / 2 ) + self.vpY
      try:
          self.framebuffer[round(pixelY)][round(pixelX)] = color or self.current_color
      except:
          pass
  
  
  
  def point(self, x, y, color = None):
     try:
       self.framebuffer[y][x] = color or self.current_color
     except:
       pass

  def triangle(self, A, B, C, color=None, texture=None, texture_coords=(), intensity=1):
    bbox_min, bbox_max = bbox(A, B, C)
    for x in range(bbox_min.x, bbox_max.x + 1):
        for y in range(bbox_min.y, bbox_max.y + 1):
            # coordenadas baricentricas
            w, v, u = barycentric(A, B, C, V2(x,y))
            # evita numeros negativos
            if (w<0) or (v<0) or (u<0):
                continue
            if texture:
                #valores para la coordenadas, que esten el el obj
                tA, tB, tC = texture_coords
                tx = tA.x * w + tB.x * v + tC.x * u
                ty = tA.y * w + tB.y * v + tC.y * u
                color = texture.intensity(tx, ty, intensity)

            z = A.z * w + B.z * v + C.z * u
            if (x<0) or (y<0):
                continue
            if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                self.point(x, y, color)
                self.zbuffer[x][y] = z

#Uso de matrices

  def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    #Mandamos los datos
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)
    #Matriz de translacion
    translatenMatrix = [
        [1, 0, 0, translate.x],
        [0, 1, 0, translate.y],
        [0, 0, 1, translate.z],
        [0, 0, 0, 1],
    ]
    #Matriz de escalar
    scaleMatrix = [
        [scale.x, 0, 0, 0],
        [0, scale.y, 0, 0],
        [0, 0, scale.z, 0],
        [0, 0, 0, 1],
    ]

    rotation_x = [
        [1, 0, 0, 0],
        [0, cos(rotate.x), -sin(rotate.x), 0],
        [0, sin(rotate.x),  cos(rotate.x), 0],
        [0, 0, 0, 1]
    ]

    rotation_y = [
            [cos(rotate.y), 0, sin(rotate.y), 0],
            [0, 1, 0, 0],
            [-sin(rotate.y), 0, cos(rotate.y), 0],
            [0, 0, 0, 1]
    ]

    rotation_z = [
        [cos(rotate.z), -sin(rotate.z), 0, 0],
        [sin(rotate.z),  cos(rotate.z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    rotateMatriz = multM(multM(rotation_x, rotation_y), rotation_z)
    self.Model = multM(multM(translatenMatrix, rotateMatriz), scaleMatrix)

  def loadViewMatrix(self, x, y, z, center):
    M = [
        [x.x, x.y, x.z, 0],
        [y.x, y.y, y.z, 0],
        [z.x, z.y, z.z, 0],
        [0, 0, 0, 1]
    ]
    O = [
        [1, 0, 0, -center.x],
        [0, 1, 0, -center.y],
        [0, 0, 1, -center.z],
        [0, 0, 0, 1]
    ]
    self.View = multM(M, O)

  def loadProjectionMatrix(self, coeff):
    self.Projection = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, coeff, 1]
    ]

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport = [
        [(self.width*0.5), 0, 0, ( x+self.width*0.5)],
        [0, (self.height*0.5), 0, (y+self.height*0.5)],
        [0, 0, 128, 128],
        [0, 0, 0, 1]
    ]

    
   #Funcion para la vista
  def lookAt(self, eye, center, up):

    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))

    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix( -1 / length(sub(eye, center)))
    self.loadViewportMatrix()


  def glObjModel(self, filename, mtl=None, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0,0,0), texture=None):

    archivo = Obj(filename)
    archivo.read()
    self.light = V3(0,0,1)
    self.loadModelMatrix(translate, scale, rotate) 
    
    #Ciclo para recorrer las carras
    for face in archivo.faces:
        vcount = len(face)
        if vcount == 3:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            a = self.transform(V3(*archivo.vertices[f1]))
            b = self.transform(V3(*archivo.vertices[f2]))
            c = self.transform(V3(*archivo.vertices[f3]))
 
            vnormal = norm(cross(sub(b,a), sub(c,a)))
            intensity = dot(vnormal, self.light)
            if intensity<0:
                continue
            if texture:
                t1 = face[0][1] - 1
                t2 = face[1][1] - 1
                t3 = face[2][1] - 1
                tA = V3(*archivo.texcoords[t1])
                tB = V3(*archivo.texcoords[t2])
                tC = V3(*archivo.texcoords[t3])
                self.triangle(a,b,c, texture=texture, texture_coords=(tA,tB,tC), intensity=intensity)
            else:
                grey =round(255*intensity)
                if grey<0:
                    continue
                self.triangle(a,b,c, color=color(grey,grey,grey))
        else:
            # assuming 4
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            f4 = face[3][0] - 1   

            vertices = [
                self.transform(V3(*archivo.vertices[f1])),
                self.transform(V3(*archivo.vertices[f2])),
                self.transform(V3(*archivo.vertices[f3])),
                self.transform(V3(*archivo.vertices[f4]))
            ]

            normal = norm(cross(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))
            intensity = dot(normal, self.light)
            grey = round(255 * intensity)

            A, B, C, D = vertices 

            if not texture:
                grey = round(255 * intensity)
                if grey < 0:
                    continue
                self.triangle(A, B, C, color(grey, grey, grey))
                self.triangle(A, C, D, color(grey, grey, grey))            
            else:
                t1 = face[0][1] - 1
                t2 = face[1][1] - 1
                t3 = face[2][1] - 1
                t4 = face[3][1] - 1
                tA = V3(*archivo.texcoords[t1])
                tB = V3(*archivo.texcoords[t2])
                tC = V3(*archivo.texcoords[t3])
                tD = V3(*archivo.texcoords[t4])
                
                self.triangle(A, B, C, texture=texture, texture_coords=(tA, tB, tC), intensity=intensity)
                self.triangle(A, C, D, texture=texture, texture_coords=(tA, tC, tD), intensity=intensity)

  
  # Función para crear la imagen
  def glFinish(self, filename):
      f = open(filename, 'bw')
      # Header
      f.write(char('B'))
      f.write(char('M'))
      f.write(dword(14 + 40 + self.width * self.height * 3))
      f.write(dword(0))
      f.write(dword(14 + 40))

      #image header
      f.write(dword(40))
      f.write(dword(self.width))
      f.write(dword(self.height))
      f.write(word(1))
      f.write(word(24))
      f.write(dword(0))
      f.write(dword(self.width * self.height * 3))
      f.write(dword(0))
      f.write(dword(0))
      f.write(dword(0))
      f.write(dword(0))
      
      #pixel data

      for x in range(self.height):
          for y in range(self.width):
              f.write(self.framebuffer[x][y])

      f.close()

  #Transformacion 
  def transform(self, vector):
    nuevoVector = [[vector.x], [vector.y], [vector.z], [1]]
    #Se multiplican las matrices
    modelMultix = multM(self.Viewport, self.Projection)
    viewMultix = multM(modelMultix, self.View)
    vpMultix = multM(viewMultix, self.Model)
    vectores = multM(vpMultix, nuevoVector)
    #transformacion
    transformVector = [
        round(vectores[0][0]/vectores[3][0]),
        round(vectores[1][0]/vectores[3][0]),
        round(vectores[2][0]/vectores[3][0])
    ]
    return V3(*transformVector)