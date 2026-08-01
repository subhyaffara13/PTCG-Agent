
def _add_inc_data(name, chunksize):
    """
    Generate incremental datasets from basic data sets
    """
    points = DATASETS[name]
    ndim = points.shape[1]

    opts = None
    nmin = ndim + 2

    if name == 'some-points':
        # since Qz is not allowed, use QJ
        opts = 'QJ Pp'
    elif name == 'pathological-1':
        # include enough points so that we get different x-coordinates
        nmin = 12

    chunks = [points[:nmin]]
    for j in range(nmin, len(points), chunksize):
        chunks.append(points[j:j+chunksize])

    new_name = f"{name}-chunk-{chunksize}"
    assert new_name not in INCREMENTAL_DATASETS
    INCREMENTAL_DATASETS[new_name] = (chunks, opts)

