# pylint: disable=unused-wildcard-import
""" load an image from file
    upload it to opengl
"""

from OpenGL.GL import glGenTextures, glBindTexture, glTexParameteri, glTexImage2D, \
    GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, \
    GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_RGBA, GL_UNSIGNED_BYTE

from PIL import Image
from Resource import Resource

# for use with GLFW
def load_texture(path, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width,
                 image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture


class Texture:
    def __init__(self, file_str):
        self.file_str = file_str
        self.tex = None
        self.image = None
        self.width = 0
        self.height = 0
        self.status = Resource.EMPTY
        
    def load(self):
        try:
            image = Image.open(self.file_str)
            self.width = image.width
            self.height = image.height
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            self.image = image.convert("RGBA").tobytes()
            self.status = Resource.LOADED
        except:
            return

    def unload(self):
        self.image = None
        self.width = 0
        self.height = 0
        self.status = Resource.EMPTY

    def create(self):
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width,
                     self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image)
                    
        self.tex = tex

    def destroy(self):
        pass

    def use(self):
        glBindTexture(GL_TEXTURE_2D, self.tex)


