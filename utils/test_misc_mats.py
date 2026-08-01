
def test_misc_mats():

    mat = Matrix([[0]])

    gl = '''0'''
    glTransposed = '''0'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([[0, 1]])

    gl = '''vec2(0, 1)'''
    glTransposed = '''vec2(0, 1)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([[0, 1, 2]])

    gl = '''vec3(0, 1, 2)'''
    glTransposed = '''vec3(0, 1, 2)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([[0, 1, 2, 3]])

    gl = '''vec4(0, 1, 2, 3)'''
    glTransposed = '''vec4(0, 1, 2, 3)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([[0, 1, 2, 3, 4]])

    gl = '''float[5](0, 1, 2, 3, 4)'''
    glTransposed = '''float[5](0, 1, 2, 3, 4)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0],
[1]])

    gl = '''vec2(0, 1)'''
    glTransposed = '''vec2(0, 1)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1],
[2, 3]])

    gl = '''mat2(0, 1, 2, 3)'''
    glTransposed = '''mat2(0, 2, 1, 3)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1, 2],
[3, 4, 5]])

    gl = '''mat3x2(0, 1, 2, 3, 4, 5)'''
    glTransposed = '''mat2x3(0, 3, 1, 4, 2, 5)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1, 2, 3],
[4, 5, 6, 7]])

    gl = '''mat4x2(0, 1, 2, 3, 4, 5, 6, 7)'''
    glTransposed = '''mat2x4(0, 4, 1, 5, 2, 6, 3, 7)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1, 2, 3, 4],
[5, 6, 7, 8, 9]])

    gl = '''float[10](
   0, 1, 2, 3, 4,
   5, 6, 7, 8, 9
) /* a 2x5 matrix */'''
    glTransposed = '''float[10](
   0, 5,
   1, 6,
   2, 7,
   3, 8,
   4, 9
) /* a 5x2 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[2][5](
   float[](0, 1, 2, 3, 4),
   float[](5, 6, 7, 8, 9)
)'''
    glNestedTransposed = '''float[5][2](
   float[](0, 5),
   float[](1, 6),
   float[](2, 7),
   float[](3, 8),
   float[](4, 9)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

    mat = Matrix([
[0],
[1],
[2]])

    gl = '''vec3(0, 1, 2)'''
    glTransposed = '''vec3(0, 1, 2)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1],
[2, 3],
[4, 5]])

    gl = '''mat2x3(0, 1, 2, 3, 4, 5)'''
    glTransposed = '''mat3x2(0, 2, 4, 1, 3, 5)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1, 2],
[3, 4, 5],
[6, 7, 8]])

    gl = '''mat3(0, 1, 2, 3, 4, 5, 6, 7, 8)'''
    glTransposed = '''mat3(0, 3, 6, 1, 4, 7, 2, 5, 8)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1,  2,  3],
[4, 5,  6,  7],
[8, 9, 10, 11]])

    gl = '''mat4x3(0, 1,  2,  3, 4, 5,  6,  7, 8, 9, 10, 11)'''
    glTransposed = '''mat3x4(0, 4,  8, 1, 5,  9, 2, 6, 10, 3, 7, 11)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[ 0,  1,  2,  3,  4],
[ 5,  6,  7,  8,  9],
[10, 11, 12, 13, 14]])

    gl = '''float[15](
   0,  1,  2,  3,  4,
   5,  6,  7,  8,  9,
   10, 11, 12, 13, 14
) /* a 3x5 matrix */'''
    glTransposed = '''float[15](
   0, 5, 10,
   1, 6, 11,
   2, 7, 12,
   3, 8, 13,
   4, 9, 14
) /* a 5x3 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[3][5](
   float[]( 0,  1,  2,  3,  4),
   float[]( 5,  6,  7,  8,  9),
   float[](10, 11, 12, 13, 14)
)'''
    glNestedTransposed = '''float[5][3](
   float[](0, 5, 10),
   float[](1, 6, 11),
   float[](2, 7, 12),
   float[](3, 8, 13),
   float[](4, 9, 14)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

    mat = Matrix([
[0],
[1],
[2],
[3]])

    gl = '''vec4(0, 1, 2, 3)'''
    glTransposed = '''vec4(0, 1, 2, 3)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1],
[2, 3],
[4, 5],
[6, 7]])

    gl = '''mat2x4(0, 1, 2, 3, 4, 5, 6, 7)'''
    glTransposed = '''mat4x2(0, 2, 4, 6, 1, 3, 5, 7)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0,  1,  2],
[3,  4,  5],
[6,  7,  8],
[9, 10, 11]])

    gl = '''mat3x4(0,  1,  2, 3,  4,  5, 6,  7,  8, 9, 10, 11)'''
    glTransposed = '''mat4x3(0, 3, 6,  9, 1, 4, 7, 10, 2, 5, 8, 11)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[ 0,  1,  2,  3],
[ 4,  5,  6,  7],
[ 8,  9, 10, 11],
[12, 13, 14, 15]])

    gl = '''mat4( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15)'''
    glTransposed = '''mat4(0, 4,  8, 12, 1, 5,  9, 13, 2, 6, 10, 14, 3, 7, 11, 15)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[ 0,  1,  2,  3,  4],
[ 5,  6,  7,  8,  9],
[10, 11, 12, 13, 14],
[15, 16, 17, 18, 19]])

    gl = '''float[20](
   0,  1,  2,  3,  4,
   5,  6,  7,  8,  9,
   10, 11, 12, 13, 14,
   15, 16, 17, 18, 19
) /* a 4x5 matrix */'''
    glTransposed = '''float[20](
   0, 5, 10, 15,
   1, 6, 11, 16,
   2, 7, 12, 17,
   3, 8, 13, 18,
   4, 9, 14, 19
) /* a 5x4 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[4][5](
   float[]( 0,  1,  2,  3,  4),
   float[]( 5,  6,  7,  8,  9),
   float[](10, 11, 12, 13, 14),
   float[](15, 16, 17, 18, 19)
)'''
    glNestedTransposed = '''float[5][4](
   float[](0, 5, 10, 15),
   float[](1, 6, 11, 16),
   float[](2, 7, 12, 17),
   float[](3, 8, 13, 18),
   float[](4, 9, 14, 19)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

    mat = Matrix([
[0],
[1],
[2],
[3],
[4]])

    gl = '''float[5](0, 1, 2, 3, 4)'''
    glTransposed = '''float[5](0, 1, 2, 3, 4)'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed

    mat = Matrix([
[0, 1],
[2, 3],
[4, 5],
[6, 7],
[8, 9]])

    gl = '''float[10](
   0, 1,
   2, 3,
   4, 5,
   6, 7,
   8, 9
) /* a 5x2 matrix */'''
    glTransposed = '''float[10](
   0, 2, 4, 6, 8,
   1, 3, 5, 7, 9
) /* a 2x5 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[5][2](
   float[](0, 1),
   float[](2, 3),
   float[](4, 5),
   float[](6, 7),
   float[](8, 9)
)'''
    glNestedTransposed = '''float[2][5](
   float[](0, 2, 4, 6, 8),
   float[](1, 3, 5, 7, 9)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

    mat = Matrix([
[ 0,  1,  2],
[ 3,  4,  5],
[ 6,  7,  8],
[ 9, 10, 11],
[12, 13, 14]])

    gl = '''float[15](
   0,  1,  2,
   3,  4,  5,
   6,  7,  8,
   9, 10, 11,
   12, 13, 14
) /* a 5x3 matrix */'''
    glTransposed = '''float[15](
   0, 3, 6,  9, 12,
   1, 4, 7, 10, 13,
   2, 5, 8, 11, 14
) /* a 3x5 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[5][3](
   float[]( 0,  1,  2),
   float[]( 3,  4,  5),
   float[]( 6,  7,  8),
   float[]( 9, 10, 11),
   float[](12, 13, 14)
)'''
    glNestedTransposed = '''float[3][5](
   float[](0, 3, 6,  9, 12),
   float[](1, 4, 7, 10, 13),
   float[](2, 5, 8, 11, 14)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

    mat = Matrix([
[ 0,  1,  2,  3],
[ 4,  5,  6,  7],
[ 8,  9, 10, 11],
[12, 13, 14, 15],
[16, 17, 18, 19]])

    gl = '''float[20](
   0,  1,  2,  3,
   4,  5,  6,  7,
   8,  9, 10, 11,
   12, 13, 14, 15,
   16, 17, 18, 19
) /* a 5x4 matrix */'''
    glTransposed = '''float[20](
   0, 4,  8, 12, 16,
   1, 5,  9, 13, 17,
   2, 6, 10, 14, 18,
   3, 7, 11, 15, 19
) /* a 4x5 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[5][4](
   float[]( 0,  1,  2,  3),
   float[]( 4,  5,  6,  7),
   float[]( 8,  9, 10, 11),
   float[](12, 13, 14, 15),
   float[](16, 17, 18, 19)
)'''
    glNestedTransposed = '''float[4][5](
   float[](0, 4,  8, 12, 16),
   float[](1, 5,  9, 13, 17),
   float[](2, 6, 10, 14, 18),
   float[](3, 7, 11, 15, 19)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

    mat = Matrix([
[ 0,  1,  2,  3,  4],
[ 5,  6,  7,  8,  9],
[10, 11, 12, 13, 14],
[15, 16, 17, 18, 19],
[20, 21, 22, 23, 24]])

    gl = '''float[25](
   0,  1,  2,  3,  4,
   5,  6,  7,  8,  9,
   10, 11, 12, 13, 14,
   15, 16, 17, 18, 19,
   20, 21, 22, 23, 24
) /* a 5x5 matrix */'''
    glTransposed = '''float[25](
   0, 5, 10, 15, 20,
   1, 6, 11, 16, 21,
   2, 7, 12, 17, 22,
   3, 8, 13, 18, 23,
   4, 9, 14, 19, 24
) /* a 5x5 matrix */'''

    assert glsl_code(mat) == gl
    assert glsl_code(mat,mat_transpose=True) == glTransposed
    glNested = '''float[5][5](
   float[]( 0,  1,  2,  3,  4),
   float[]( 5,  6,  7,  8,  9),
   float[](10, 11, 12, 13, 14),
   float[](15, 16, 17, 18, 19),
   float[](20, 21, 22, 23, 24)
)'''
    glNestedTransposed = '''float[5][5](
   float[](0, 5, 10, 15, 20),
   float[](1, 6, 11, 16, 21),
   float[](2, 7, 12, 17, 22),
   float[](3, 8, 13, 18, 23),
   float[](4, 9, 14, 19, 24)
)'''

    assert glsl_code(mat,mat_nested=True) == glNested
    assert glsl_code(mat,mat_nested=True,mat_transpose=True) == glNestedTransposed

