
def get_path_collection_extents(
        master_transform, paths, transforms, offsets, offset_transform):
    r"""
    Get bounding box of a `.PathCollection`\s internal objects.

    That is, given a sequence of `Path`\s, `.Transform`\s objects, and offsets, as found
    in a `.PathCollection`, return the bounding box that encapsulates all of them.

    Parameters
    ----------
    master_transform : `~matplotlib.transforms.Transform`
        Global transformation applied to all paths.
    paths : list of `Path`
    transforms : list of `~matplotlib.transforms.Affine2DBase`
        If non-empty, this overrides *master_transform*.
    offsets : (N, 2) array-like
    offset_transform : `~matplotlib.transforms.Affine2DBase`
        Transform applied to the offsets before offsetting the path.

    Notes
    -----
    The way that *paths*, *transforms* and *offsets* are combined follows the same
    method as for collections: each is iterated over independently, so if you have 3
    paths (A, B, C), 2 transforms (α, β) and 1 offset (O), their combinations are as
    follows:

    - (A, α, O)
    - (B, β, O)
    - (C, α, O)
    """
    from .transforms import Bbox
    if len(paths) == 0:
        raise ValueError("No paths provided")
    if len(offsets) == 0:
        raise ValueError("No offsets provided")
    extents, minpos = _path.get_path_collection_extents(
        master_transform, paths, np.atleast_3d(transforms),
        offsets, offset_transform)
    return Bbox.from_extents(*extents, minpos=minpos)

