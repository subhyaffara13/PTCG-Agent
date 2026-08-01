
def init_gl_modern(display_size):
    """
    Initialise open GL in the 'modern' open GL style for open GL versions
    greater than 3.1.

    :param display_size: Size of the window/viewport.
    """

    # Create shaders
    # --------------------------------------
    vertex_code = """

    #version 150
    uniform mat4   model;
    uniform mat4   view;
    uniform mat4   projection;

    uniform vec4   colour_mul;
    uniform vec4   colour_add;

    in vec4 vertex_colour;         // vertex colour in
    in vec3 vertex_position;

    out vec4   vertex_color_out;            // vertex colour out
    void main()
    {
        vertex_color_out = (colour_mul * vertex_colour) + colour_add;
        gl_Position = projection * view * model * vec4(vertex_position, 1.0);
    }

    """

    fragment_code = """
    #version 150
    in vec4 vertex_color_out;  // vertex colour from vertex shader
    out vec4 fragColor;
    void main()
    {
        fragColor = vertex_color_out;
    }
    """

    program = GL.glCreateProgram()
    vertex = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    fragment = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(vertex, vertex_code)
    GL.glCompileShader(vertex)

    # this logs issues the shader compiler finds.
    log = GL.glGetShaderInfoLog(vertex)
    if isinstance(log, bytes):
        log = log.decode()
    for line in log.split("\n"):
        print(line)

    GL.glAttachShader(program, vertex)
    GL.glShaderSource(fragment, fragment_code)
    GL.glCompileShader(fragment)

    # this logs issues the shader compiler finds.
    log = GL.glGetShaderInfoLog(fragment)
    if isinstance(log, bytes):
        log = log.decode()
    for line in log.split("\n"):
        print(line)

    GL.glAttachShader(program, fragment)
    GL.glValidateProgram(program)
    GL.glLinkProgram(program)

    GL.glDetachShader(program, vertex)
    GL.glDetachShader(program, fragment)
    GL.glUseProgram(program)

    # Create vertex buffers and shader constants
    # ------------------------------------------

    # Cube Data
    vertices = zeros(
        8, [("vertex_position", float32, 3), ("vertex_colour", float32, 4)]
    )

    vertices["vertex_position"] = [
        [1, 1, 1],
        [-1, 1, 1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, -1],
    ]

    vertices["vertex_colour"] = [
        [0, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 1, 0, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 1],
    ]

    filled_cube_indices = array(
        [
            0,
            1,
            2,
            0,
            2,
            3,
            0,
            3,
            4,
            0,
            4,
            5,
            0,
            5,
            6,
            0,
            6,
            1,
            1,
            6,
            7,
            1,
            7,
            2,
            7,
            4,
            3,
            7,
            3,
            2,
            4,
            7,
            6,
            4,
            6,
            5,
        ],
        dtype=uint32,
    )

    outline_cube_indices = array(
        [0, 1, 1, 2, 2, 3, 3, 0, 4, 7, 7, 6, 6, 5, 5, 4, 0, 5, 1, 6, 2, 7, 3, 4],
        dtype=uint32,
    )

    shader_data = {"buffer": {}, "constants": {}}

    GL.glBindVertexArray(GL.glGenVertexArrays(1))  # Have to do this first

    shader_data["buffer"]["vertices"] = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, shader_data["buffer"]["vertices"])
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    loc = GL.glGetAttribLocation(program, "vertex_position")
    GL.glEnableVertexAttribArray(loc)
    GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, stride, offset)

    offset = ctypes.c_void_p(vertices.dtype["vertex_position"].itemsize)

    loc = GL.glGetAttribLocation(program, "vertex_colour")
    GL.glEnableVertexAttribArray(loc)
    GL.glVertexAttribPointer(loc, 4, GL.GL_FLOAT, False, stride, offset)

    shader_data["buffer"]["filled"] = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["filled"])
    GL.glBufferData(
        GL.GL_ELEMENT_ARRAY_BUFFER,
        filled_cube_indices.nbytes,
        filled_cube_indices,
        GL.GL_STATIC_DRAW,
    )

    shader_data["buffer"]["outline"] = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, shader_data["buffer"]["outline"])
    GL.glBufferData(
        GL.GL_ELEMENT_ARRAY_BUFFER,
        outline_cube_indices.nbytes,
        outline_cube_indices,
        GL.GL_STATIC_DRAW,
    )

    shader_data["constants"]["model"] = GL.glGetUniformLocation(program, "model")
    GL.glUniformMatrix4fv(shader_data["constants"]["model"], 1, False, eye(4))

    shader_data["constants"]["view"] = GL.glGetUniformLocation(program, "view")
    view = translate(eye(4), z=-6)
    GL.glUniformMatrix4fv(shader_data["constants"]["view"], 1, False, view)

    shader_data["constants"]["projection"] = GL.glGetUniformLocation(
        program, "projection"
    )
    GL.glUniformMatrix4fv(shader_data["constants"]["projection"], 1, False, eye(4))

    # This colour is multiplied with the base vertex colour in producing
    # the final output
    shader_data["constants"]["colour_mul"] = GL.glGetUniformLocation(
        program, "colour_mul"
    )
    GL.glUniform4f(shader_data["constants"]["colour_mul"], 1, 1, 1, 1)

    # This colour is added on to the base vertex colour in producing
    # the final output
    shader_data["constants"]["colour_add"] = GL.glGetUniformLocation(
        program, "colour_add"
    )
    GL.glUniform4f(shader_data["constants"]["colour_add"], 0, 0, 0, 0)

    # Set GL drawing data
    # -------------------
    GL.glClearColor(0, 0, 0, 0)
    GL.glPolygonOffset(1, 1)
    GL.glEnable(GL.GL_LINE_SMOOTH)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glDepthFunc(GL.GL_LESS)
    GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
    GL.glLineWidth(1.0)

    projection = perspective(45.0, display_size[0] / float(display_size[1]), 2.0, 100.0)
    GL.glUniformMatrix4fv(shader_data["constants"]["projection"], 1, False, projection)

    return shader_data, filled_cube_indices, outline_cube_indices

