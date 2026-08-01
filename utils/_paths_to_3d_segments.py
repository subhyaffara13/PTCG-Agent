
def _paths_to_3d_segments(paths, zs=0, zdir='z'):
    """Convert paths from a collection object to 3D segments."""

    if not np.iterable(zs):
        zs = np.broadcast_to(zs, len(paths))
    else:
        if len(zs) != len(paths):
            raise ValueError('Number of z-coordinates does not match paths.')

    segs = [_path_to_3d_segment(path, pathz, zdir)
            for path, pathz in zip(paths, zs)]
    return segs

