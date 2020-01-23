# pylint: disable=unused-wildcard-import
import glfw
from OpenGL.GL import *
import pyrr

from Mesh import Mesh, Status
from Shader import Shader
from Texture import Texture
from Camera import Camera, Process_mouse
from Scene import Scene

WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True

CAM_MOVE_FOR = False
CAM_MOVE_BACK = False
CAM_MOVE_LEFT = False
CAM_MOVE_RIGHT = False
light_index = 0

cam = None # currently active scene camera

# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global CAM_MOVE_FOR, CAM_MOVE_BACK, CAM_MOVE_LEFT, CAM_MOVE_RIGHT, light_index

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_S:
        CAM_MOVE_FOR = False if action == glfw.RELEASE else True
    elif key == glfw.KEY_W:
        CAM_MOVE_BACK = False if action == glfw.RELEASE else True
    elif key == glfw.KEY_A:
        CAM_MOVE_LEFT = False if action == glfw.RELEASE else True
    elif key == glfw.KEY_D:
        CAM_MOVE_RIGHT = False if action == glfw.RELEASE else True

    elif key == glfw.KEY_PAGE_UP:
        light_pos[light_index] += .2
    elif key == glfw.KEY_PAGE_DOWN:
        light_pos[light_index] -= .2

    elif key == glfw.KEY_X:
        light_index = 0
    elif key == glfw.KEY_Y:
        light_index = 1
    elif key == glfw.KEY_Z:
        light_index = 2


# the mouse position callback function
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    if cam:
        cam.process_mouse_movement(xoffset, yoffset)


# the window resize callback function
def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(
        45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)
glfw.set_input_mode(window, glfw.STICKY_KEYS, glfw.TRUE)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize_clb)
# set the mouse position callback
glfw.set_cursor_pos_callback(window, mouse_look_clb)
# set the keyboard input callback
glfw.set_key_callback(window, key_input_clb)
# capture the mouse cursor
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

# make the context current
glfw.make_context_current(window)

# load a scene
scene = Scene("resources/scene1.json")
cam = scene.active_camera

# mesh1 = Mesh("resources/meshes/tetra2.ply")
mesh1 = Mesh("resources/meshes/tetra3_p_n_uv1.ply")
mesh1.load()
mesh1.create()
mesh1_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 2]))

mesh2 = Mesh("resources/meshes/plane2_p_n_uv1.ply")
mesh2.load()
mesh2.create()
mesh2_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

# mesh3 = Mesh("resources/meshes/Dragon.ply")
# mesh3.load()
# mesh3.create()
# mesh3_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([2, 1, .5]))

shader1 = Shader("resources/shaders/shader1.vs", "resources/shaders/shader1.fs")
shader1.load()
shader1.create()
# shader1.use() # needed

tex1 = Texture("resources/images/marble.jpg")
tex1.load()
tex1.create()

tex2 = Texture("resources/images/brickwall.jpg")
tex2.load()
tex2.create()

tex3 = Texture("resources/images/StoneMarbleCalacatta004_COL_2K.jpg")
tex3.load()
tex3.create()

cam.process_mouse_movement(0, 0)

glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glEnable(GL_CULL_FACE)
# glCullFace(GL_FRONT)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

light_pos = [0.0, 1.0, 3.0]


# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if CAM_MOVE_FOR:
        cam.pos -= .1 * cam.front
    if CAM_MOVE_BACK:
        cam.pos += .1 * cam.front
    if CAM_MOVE_LEFT:
        cam.pos -= .1 * cam.right
    if CAM_MOVE_RIGHT:
        cam.pos += .1 * cam.right

    shader = shader1
    shader.use()  # call it before mesh.use()

    projection = pyrr.matrix44.create_perspective_projection_matrix(
        45, WIDTH / HEIGHT, 0.1, 100)
    proj_loc = glGetUniformLocation(shader.program, "projection")
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    
    view = cam.get_view_matrix()
    view_loc = glGetUniformLocation(shader.program, "view")
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    light_loc = glGetUniformLocation(shader.program, "light_pos")
    glUniform3fv(light_loc, 1, light_pos)

    rot_y = pyrr.Matrix44.from_z_rotation(0.0001* glfw.get_time())
    mesh1_mat = pyrr.matrix44.multiply(rot_y, mesh1_mat)
    model_loc = glGetUniformLocation(shader.program, "model")
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, mesh1_mat)
    tex1.use()
    mesh1.use()
    
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, mesh2_mat)
    tex2.use()
    mesh2.use()

    # glUniformMatrix4fv(model_loc, 1, GL_FALSE, mesh3_mat)
    # tex3.use()
    # mesh3.use()

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
