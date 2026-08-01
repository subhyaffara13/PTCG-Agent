
def gen_oa_shapes_2d(sizes):
    shapes0 = gen_oa_shapes(sizes)
    shapes1 = gen_oa_shapes(sizes)
    shapes = [ishapes0+ishapes1 for ishapes0, ishapes1 in
              zip(shapes0, shapes1)]

    modes = ['full', 'valid', 'same']
    return [ishapes+(imode,) for ishapes, imode in product(shapes, modes)
            if imode != 'valid' or
            (ishapes[0] > ishapes[1] and ishapes[2] > ishapes[3]) or
            (ishapes[0] < ishapes[1] and ishapes[2] < ishapes[3])]

