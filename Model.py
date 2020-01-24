'''
A model bundles all information which is needed to render a 3d-model
    1. mesh file
    2. shader files
    3. texture files
    4. coordinate system (position, orientation, scale) a.k.a TRS

    5. a affected_by_lights list, these are the dynamic light that are
    taken into account whilst shading. To include more lights than e.g. 4
    would be to expensive considering perfomance.
'''

class Model:
    def __init__(self, data):
        self.io = data

        self.mesh = None
        self.shader = None
        self.textures = {
            'diffuse': None,
            'specular': None,
            'normal': None,
            'lightmap': None,
            # 'whatever': None,
        }
        self.material = {
            'ambient': [0.1, 0.1, 0.1],
            'diffuse': [1.0, 1.0, 1.0],
            'specular': [1.0, 1.0, 1.0],
            'shinyness': 0.2
        }

        self.pos = data['frame']['pos']
        self.quat = data['frame']['quat']

    def load(self):
        self.mesh.load()
        self.shader.load()
        for tex in self.textures.values():
            tex.load()

    def create(self):
        self.mesh.create()
        self.shader.create()
        for tex in self.textures.values():
            tex.create()

    def use(self):
        self.shader.use()
        self.mesh.use()
        for tex in self.textures.values():
            tex.use()
