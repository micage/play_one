import json
from Camera import Camera

'''
A scene is a collectioon of models, lights and cameras
'''

class Scene:
    def __init__(self, file_name):
        self.models = None
        self.cameras = None
        self.lights = None
        self.active_camera = Camera()
    
        with open("resources/scene1.json", "r") as fp:
            data = json.load(fp)
            self.models = data["models"]
            self.lights = data["cameras"]
            self.models = data["lights"]
        

