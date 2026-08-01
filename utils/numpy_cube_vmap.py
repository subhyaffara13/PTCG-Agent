
def numpy_cube_vmap(info, in_dims, x):
    result = numpy_cube(x)
    return result, (in_dims[0], in_dims[0])

