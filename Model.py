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
    def __init__(self):
        self.mesh = None
        self.vert = None
        self.frag = None
        self.texture = None

