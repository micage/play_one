# version 330

layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 uv1;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;
uniform vec3 light_pos;

out vec2 v_texture;
out vec3 surface_normal;
out vec3 to_light;
out vec3 cam_pos;

void main()
{
    vec4 world_position = model * vec4(pos, 1.0);
    
    gl_Position = projection * view * world_position;
    v_texture = uv1;

    // need transpose(inverse(model)) here instead of just model
    surface_normal = (transpose(inverse(model)) * vec4(normal, 1.0)).xyz;
    
    to_light = light_pos - world_position.xyz;
    
    // cam_pos = vec3(-view[0].w, -view[1].w, -view[2].w);
    cam_pos = (inverse(view) * vec4(0.0, 0.0, 0.0, 1.0)).xyz;

}