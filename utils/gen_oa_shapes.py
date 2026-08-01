
def gen_oa_shapes(sizes):
    return [(a, b) for a, b in product(sizes, repeat=2)
            if abs(a - b) > 3]

