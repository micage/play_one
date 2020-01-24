import json
import logging
from Model import Model
from Camera import Camera
from Light import Light
from Mesh import Mesh
from Shader import Shader
from Texture import Texture
import ResourceManager

'''
A scene is a collectioon of models, lights and cameras
'''

active_camera = Camera({})

class Scene:
    def __init__(self, file_name):
        global active_camera
        self.models = None
        self.cameras = None
        self.lights = None
        self.active_camera = active_camera

        # shared resources
        self.textures = {} # name -> tex lookup
        self.shaders = {} # name -> tex lookup
        self.meshes = {} # name -> tex lookup
    
        with open(file_name, "r") as fp:
            data = json.load(fp)

        # models
        self.models = {name: Model(m) for (name, m) in data["models"].items()}
        for model in self.models.values():
            vert_file = model.io['shader']['vert']
            frag_file = model.io['shader']['frag']
            shader_name = vert_file.split('.')[0]
            shader = ResourceManager.get_shader(shader_name)
            if not shader:
                shader = Shader(vert_file, frag_file)
                ResourceManager.add_shader(shader_name, shader)
            model.shader = shader

            mesh_name = model.io['mesh'] # contains relative path string
            mesh = ResourceManager.get_mesh(mesh_name)
            if not mesh:
                mesh = Mesh(mesh_name)
                ResourceManager.add_mesh(mesh_name, mesh)
            model.mesh = mesh

            tex_files = model.io['textures']
            for (layer, tex_file) in tex_files.items():
                tex = ResourceManager.get_texture(tex_file)
                if not tex:
                    tex = Texture(tex_file)
                    ResourceManager.add_texture(tex_file, tex)
                model.textures[layer] = tex

        # cameras, set first camera to active
        self.cameras = {name: Camera(c)
                        for (name, c) in data["cameras"].items()}
        if len(self.cameras) > 0:
            # get first items value
            active_camera = next(iter(self.cameras.items()))[1]
        logging.warn('camera needs to set shader uniforms')

        # lights
        self.lights = {name: Light(l) for (name, l) in data["lights"].items()}
        logging.warn('light needs to set shader uniforms')
            

    def load(self):
        for model in self.models:
            model.load()

    def create(self):
        for model in self.models:
            model.create()

    def render(self):
        for model in self.models:
            model.use()

    def set_active_camera(self, name):
        global active_camera
        cam = self.cameras.get(name)
        if not cam:
            logging.error(f'Camera {name} does not exist.')
            return
        active_camera = cam
