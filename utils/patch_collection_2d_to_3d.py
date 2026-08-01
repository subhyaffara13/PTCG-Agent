
def patch_collection_2d_to_3d(
    col,
    zs=0,
    zdir="z",
    depthshade=None,
    axlim_clip=False,
    *args,
    depthshade_minalpha=None,
):
    """
    Convert a `.PatchCollection` into a `.Patch3DCollection` object
    (or a `.PathCollection` into a `.Path3DCollection` object).

    Parameters
    ----------
    col : `~matplotlib.collections.PatchCollection` or \
`~matplotlib.collections.PathCollection`
        The collection to convert.
    zs : float or array of floats
        The location or locations to place the patches in the collection along
        the *zdir* axis. Default: 0.
    zdir : {'x', 'y', 'z'}
        The axis in which to place the patches. Default: "z".
        See `.get_dir_vector` for a description of the values.
    depthshade : bool, default: :rc:`axes3d.depthshade`
        Whether to shade the patches to give a sense of depth.
    axlim_clip : bool, default: False
        Whether to hide patches with a vertex outside the axes view limits.

        .. versionadded:: 3.10

    depthshade_minalpha : float, default: :rc:`axes3d.depthshade_minalpha`
        Sets the minimum alpha value used by depth-shading.

        .. versionadded:: 3.11
    """
    if isinstance(col, PathCollection):
        col.__class__ = Path3DCollection
        col._offset_zordered = None
    elif isinstance(col, PatchCollection):
        col.__class__ = Patch3DCollection
    if depthshade is None:
        depthshade = rcParams['axes3d.depthshade']
    if depthshade_minalpha is None:
        depthshade_minalpha = rcParams['axes3d.depthshade_minalpha']
    col._depthshade = depthshade
    col._depthshade_minalpha = depthshade_minalpha
    col._in_draw = False
    col.set_3d_properties(zs, zdir, axlim_clip)

