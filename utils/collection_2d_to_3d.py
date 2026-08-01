
def collection_2d_to_3d(col, zs=0, zdir='z', axlim_clip=False):
    """Convert a `.Collection` to a `.Collection3D` object."""
    zs = np.broadcast_to(zs, len(col.get_paths()))
    col._3dverts_codes = [
        (np.column_stack(juggle_axes(
            *np.column_stack([p.vertices, np.broadcast_to(z, len(p.vertices))]).T,
            zdir)),
         p.codes)
        for p, z in zip(col.get_paths(), zs)]
    col.__class__ = cbook._make_class_factory(Collection3D, "{}3D")(type(col))
    col._axlim_clip = axlim_clip

