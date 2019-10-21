uniform sampler2D u_texture;
varying vec2 v_texcoord;

vec3 hsv2rgb(float h, float s, float v)
{
    float c = s; // float c = v * s;
    float h2 = h / 60.0;
    float x = c * (1.0 - abs(mod(h2, 2.0) - 1.0));
    vec3 rgb = (v - c) * vec3(1.0, 1.0, 1.0);

    if (0.0 <= h2 && h2 < 1.0) {
        rgb += vec3(c, x, 0.0);
    } else if (1.0 <= h2 && h2 < 2.0) {
        rgb += vec3(x, c, 0.0);
    } else if (2.0 <= h2 && h2 < 3.0) {
        rgb += vec3(0.0, c, x);
    } else if (3.0 <= h2 && h2 < 4.0) {
        rgb += vec3(0.0, x, c);
    } else if (4.0 <= h2 && h2 < 5.0) {
        rgb += vec3(x, 0.0, c);
    } else if (5.0 <= h2 && h2 < 6.0) {
        rgb += vec3(c, 0.0, x);
    }

    return rgb;
}

void main()
{
    float r = texture2D(u_texture, v_texcoord).r;
    gl_FragColor = vec4(hsv2rgb(r, 1.0, 1.0), 1.0);
}