'''
A material holds all information about how the surface of a mesh
reacts to light
'''

class Material:
    def __init__(self):
        self.ambient = [1.0, 1.0, 1.0]
        self.diffuse = [1.0, 1.0, 1.0, 1.0] # last value is transparency
        self.specular = [1.0,1.0, 1.0]
        self.tex_diffuse = None
        self.tex_specular = None
        self.tex_normal = None
        self.tex_lightmap = None