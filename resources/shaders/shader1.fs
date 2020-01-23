# version 330

in vec2 v_texture;
in vec3 surface_normal;
in vec3 to_light;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    vec3 N0 = normalize(surface_normal);
    vec3 L0 = normalize(to_light);
    float dot_NL = dot(N0, L0);
    float b = max(dot_NL, 0.0);
    vec3 c = b * vec3(0.9, 1.0, 1.0);
    // vesc3 c = .5 * N0 + vec3(1.0, 1.0, 1.0);
    // vec3 c = .5 * L0 + vec3(1.0, 1.0, 1.0);

    out_color = vec4(c, 1.0) * texture(s_texture, v_texture);
}
