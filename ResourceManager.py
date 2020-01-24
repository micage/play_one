'''
The ResourceManager keeps track of textures, meshes and shaders.
It's just 3 dictionaries that ensures that we do not load or create 
a resource twice since it could be used by several models in a scene.
'''


shaders = {}
textures = {}
meshes = {}


def add_texture(name, tex):
    textures[name] = tex


def get_texture(name):
    return textures.get(name)


def add_mesh(name, mesh):
    meshes[name] = mesh


def get_mesh(name):
    return meshes.get(name)


def add_shader(name, shader):
    shaders[name] = shader


def get_shader(name):
    return shaders.get(name)
