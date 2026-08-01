
def gen_oa_shapes_eq(sizes):
    return [(a, b) for a, b in product(sizes, repeat=2)
            if a >= b]

