
def _generate_sample_shape_reduction():
    shapes = ((S,), (S, S), (S, S, S))
    reductions = ('none', 'mean', 'sum')
    yield from product(shapes, reductions)

