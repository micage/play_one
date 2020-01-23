from enum import Flag

'''
A light describes the properties of a dynamic light source. 
It has a
    type LightType
    position, direction in world space coords (depending on its type)
    color (RGB) which length is also the intensity of the light
    attenuation (constant, linear, quadratic)
'''

class LightType(Flag):
    POINT = 1
    DIRECTIONAL = 2
    SPOT = 7
    SPOTSOFT = 15


class Light:
    def __init__(self):
        self.type = LightType.DIRECTIONAL
        self.color = [1.0, 1.0, 1.0]
        self.attenuation = [1.0, 0.0, 0.0]
        self.dir = [0.0, -1.0, 0.0]
        self.pos = [0.0, 10.0, 0.0]

