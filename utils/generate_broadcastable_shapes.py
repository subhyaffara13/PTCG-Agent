
def generate_broadcastable_shapes(nshapes, *, ndim=2, min=0, max=10, rng=None):
    rng = np.random.default_rng(rng)
    min = np.broadcast_to(min, ndim)  # so min and max can be scalars or array-like 
    max = np.broadcast_to(max, ndim)
    batch_shape = tuple(rng.integers(min_, max_+1) for min_, max_ in zip(min, max))
    shapes = np.repeat([batch_shape], nshapes, axis=0)

    # make some elements of some shapes 1 (while preserving overall batch shape)
    for column in shapes.T:
        column[rng.integers(1, nshapes):] = 1
    # permute elements between shapes (while preserving overall batch shape)
    shapes = list(rng.permuted(shapes, axis=0))
    # potentially trim preceeding 1s from a shape
    for i in range(len(shapes)):
        shape = shapes[i]
        j = np.where(shape != 1)[0][0] if np.any(shape != 1) else ndim
        if rng.random() < 0.25:
            shapes[i] = shape[rng.integers(j+1):]
            break

    assert np.broadcast_shapes(*shapes) == batch_shape
    return [tuple(int(el) for el in shape) for shape in shapes]

