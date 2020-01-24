# pylint: disable=unused-wildcard-import

from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

mouse_sensitivity = 0.1


def Process_mouse(cam, jaw, pitch, xoffset, yoffset, constrain_pitch=True):
    global mouse_sensitivity

    xoffset *= mouse_sensitivity
    yoffset *= mouse_sensitivity

    jaw -= xoffset
    pitch += yoffset

    if constrain_pitch:
        if pitch > 80:
            pitch = 80
        if pitch < -80:
            pitch = -80

    return jaw, pitch

def Axis_from_jaw_pitch(jaw, pitch): 
    front = Vector3([0.0, 0.0, 0.0])

    # jaw, pitch are spherical coordinates that define a unit vector
    front.x = cos(radians(jaw)) * cos(radians(pitch))
    front.z = sin(radians(pitch))
    front.y = sin(radians(jaw)) * cos(radians(pitch))

    right = vector3.cross(front, Vector3([0.0, 0.0, 1.0]))
    up = vector3.cross(right, front)

    return (front, right, up)

class Camera:
    def __init__(self, data):
        self.pos = Vector3([0.0, 8.0, 2.0])
        self.right = Vector3([1.0, 0.0, 0.0])
        self.up = Vector3([0.0, 0.0, 1.0])
        self.front = Vector3([0.0, 1.0, 0.0])

        self.mouse_sensitivity = 0.1
        self.jaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.pos, self.pos + self.front, self.up)

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw -= xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 80:
                self.pitch = 80
            if self.pitch < -80:
                self.pitch = -80

        self.update_vectors()

    def update_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.z = sin(radians(self.pitch))
        front.y = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.front = vector.normalise(front)
        self.right = vector.normalise(vector3.cross(
            self.front, Vector3([0.0, 0.0, 1.0])))
        self.up = vector.normalise(vector3.cross(self.right, self.front))
