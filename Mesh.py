# pylint: disable=unused-wildcard-import

'''
list<vertex>
    vertex
        position
            x y z
        color (optional)
            r g b a
        normal (optional)
            x y z
        uv_1 # texture coordinates
            u v
        ...
list<triangle> # 3 vertex indices
    triangle
        i1 i2 i3
'''

from OpenGL.GL import *
from enum import Flag
from plyfile import PlyData, PlyElement
import numpy as np

class Status(Flag):
    EMPTY = 0
    LOADED = 1
    CREATED = 2
    def set(self, flag, bit):
        flag |= bit
    def unset(self, flag, bit):
        flag &= ~bit


def parse_props(line_it):
    line = next(line_it)
    while (line.find("end_header") == -1):
        parts = line.split(' ')
        if parts[0] == 'element':
            line = parse_props(line_it)
            continue
        try:
            line = next(line_it)
        except:
            break
    return line

# helper
def parse_ply(line_it):
    ''' find element -> elem_name -> elem_count '''
    ret = {}
    line = next(line_it)[:-1]
    print(line)

    while (line.find("end_header") == -1):
        parts = line.split(' ')
        if parts[0] == 'element':
            ret[parts[1]] = parts[2]
            line = parse_props(line_it)
            continue
        try:
            line = next(line_it)
        except:
            break
    return ret


def parse_vertex(line_it):
    pass


def parse_triangle(line_it):
    pass


class Mesh:
    def __init__(self, mesh_file):
        self._file = mesh_file
        self._verts = None
        self._faces = None
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.stride = 0
        self.status = Status.EMPTY
        self.num_faces = 0
        self.has_normals = False
        self.has_uv1 = False
        self.has_uv2 = False
        self.attributes = []

    ''' loads a shader from a *.vs file and a *.fs file '''
    def load(self):
        with open(self._file, "rb") as f:
            # self._str = f.readlines()     
            # self._str = [line for line in f]
            # line_it = iter(f)
            # result = parse_ply(line_it)
            try:
                Ply = PlyData.read(f)
            except:
                return

            '''
            get vertex attribute info (position, normal, color, uv1, uv2, ... ):
                name: {                     
                    data:
                    size: size of each attr
                    offset: buffer offset in bytes after flattening
                }
            '''

            verts = Ply['vertex']
            verts_data = Ply['vertex'].data
            props = [p.name for p in verts.properties]

            attrs = [('x', 'y', 'z'), ('nx', 'ny', 'nz'), ('s' 't')]
            index = 0

            # position
            pos_attr = ['x', 'y', 'z']
            if len(pos_attr) != sum(int(a == p) for p in props for a in pos_attr):
                self.unload()
                return
            self.attributes.append({
                'count': 3,
                'index': 0
            })
            index += 1

            # normals
            normal_attr = ['nx', 'ny', 'nz']
            if sum(int(a == p) for p in props for a in normal_attr) == 3:
                self.attributes.append({
                    'count': len(normal_attr),
                    'index': index
                })
                index += 1

            # uv1
            uv1_attr = ['s', 't']
            if sum(int(a == p) for p in props for a in uv1_attr) == 2:
                self.attributes.append({
                    'count': 2,
                    'index': index
                })
                index += 1

            props_data = [verts_data[i] for i in props]
            self._verts = np.dstack(props_data).flatten()
            self.stride = int(self._verts.nbytes / Ply['vertex'].count)
            self.num_faces = Ply['face'].count

            self._faces = np.hstack(Ply['face']['vertex_indices'])

            self.status |= Status.LOADED # self.status.set(Status.LOADED)

    def unload(self):
        self._verts = None
        self._faces = None
        self.status &= ~Status.LOADED  # self.status.set(Status.LOADED)

    
    def create(self):
        if not(self.status & Status.LOADED):
            return

        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindVertexArray(VAO)

        # draw_mode: (GL_STATIC_DRAW, GL_DYNAMIC_DRAW, GL_STREAM_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self._verts.nbytes, self._verts, GL_STATIC_DRAW)

        offset = 0
        for attr in self.attributes:
            glEnableVertexAttribArray(attr['index'])
            glVertexAttribPointer(attr['index'], attr['count'],
                GL_FLOAT, GL_FALSE,
                self.stride, ctypes.c_void_p(offset))
            offset += attr['count'] * 4 # size of float in bytes


        # # position
        # glEnableVertexAttribArray(index)
        # glVertexAttribPointer(index, 3, GL_FLOAT, GL_FALSE,
        #                       self.stride, ctypes.c_void_p(offset))
        # offset += 12
        # index += 1

        # # normals
        # if self.has_normals:
        #     glEnableVertexAttribArray(index)
        #     glVertexAttribPointer(index, 3, GL_FLOAT, GL_FALSE,
        #                           self.stride, ctypes.c_void_p(offset))
        #     offset += 12
        #     index += 1

        # # uv1
        # if self.has_uv1:
        #     glEnableVertexAttribArray(index)
        #     glVertexAttribPointer(index, 2, GL_FLOAT, GL_FALSE,
        #                           self.stride, ctypes.c_void_p(offset))
        #     offset += 8
        #     index += 1

        # Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._faces.nbytes, self._faces, GL_STATIC_DRAW)

        self.VAO = VAO
        self.VBO = VBO
        self.EBO = VBO
        self.status |= Status.CREATED
    
    def delete(self):
        glDeleteBuffers(1, self.VBO)
        self.VBO = 0
        glDeleteVertexArrays(1, self.VAO)
        self.VAO = 0
        self.status &= ~Status.CREATED

    def use(self):
        if self.status & Status.CREATED:
            glBindVertexArray(self.VAO)
            glDrawElements(GL_TRIANGLES, self.num_faces * 3, GL_UNSIGNED_INT, None)

        
