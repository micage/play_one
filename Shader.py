# pylint: disable=unused-wildcard-import
from OpenGL.GL import glCreateShader, glShaderSource, glCompileShader, glGetShaderiv, \
    glCreateProgram, glAttachShader, glLinkProgram, glDeleteProgram, glUseProgram, \
    glValidateProgram, glGetProgramInfoLog, glGetProgramiv, glGetShaderInfoLog, \
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_LINK_STATUS, GL_TRUE, GL_FALSE, \
    GL_VALIDATE_STATUS, GL_COMPILE_STATUS
from enum import Flag


class Status(Flag):
    EMPTY = 0
    LOADED = 1
    CREATED = 2
    def set(self, flag, bit):
        flag |= bit
    def unset(self, flag, bit):
        flag &= ~bit

class Shader:
    def __init__(self, vs_file, fs_file):
        self.vs_file = vs_file
        self.fs_file = fs_file
        self.vs_str = None
        self.fs_str = None
        self.program = None
        self.status = Status.EMPTY

    def load(self):
        ''' loads a shader from a *.vs file and a *.fs file '''
        with open(self.vs_file, "rb") as f:
            self.vs_str = f.read()

        with open(self.fs_file, "rb") as f:
            self.fs_str = f.read()

        if self.vs_str and self.fs_str:
            self.status |= Status.LOADED # self.status.set(Status.LOADED)
        else:
            self.unload()

    def unload(self):
        self.vs_str = None
        self.fs_str = None
        self.status &= ~Status.LOADED  # self.status.set(Status.LOADED)

    def create(self):
        if not(self.status & Status.LOADED):
            return

        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, self.vs_str)
        glCompileShader(vs)
        if glGetShaderiv(vs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(vs))

        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, self.fs_str)
        glCompileShader(fs)
        if glGetShaderiv(fs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(fs))

        program = glCreateProgram()
        glAttachShader(program, vs)
        glAttachShader(program, fs)

        glLinkProgram(program)
       	if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(program))

        glValidateProgram(program)
        validation = glGetProgramiv(program, GL_VALIDATE_STATUS)
        if validation == GL_FALSE:
            raise RuntimeError(glGetProgramInfoLog(program))

        # todo: check for errrors before setting status
        self.program = program
        self.status |= Status.CREATED
    
    def delete(self):
        glDeleteProgram(self.program)
        self.program = 0
        self.status &= ~Status.CREATED

    def use(self):
        if self.status & Status.CREATED:
            glUseProgram(self.program)

        
