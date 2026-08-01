
def _apply_scale_transforms(xs, ys, zs, axes):
    """
    Apply axis scale transforms to 3D coordinates.

    Transforms data coordinates to transformed coordinates (applying log,
    symlog, etc.) for 3D projection. Preserves masked arrays.
    """
    def transform_coord(coord, axis):
        coord = np.asanyarray(coord)
        data = np.ma.getdata(coord).ravel()
        return axis.get_transform().transform(data).reshape(coord.shape)

    xs_scaled = transform_coord(xs, axes.xaxis)
    ys_scaled = transform_coord(ys, axes.yaxis)
    zs_scaled = transform_coord(zs, axes.zaxis)

    # Preserve combined mask from any masked input
    masks = [np.ma.getmask(a) for a in [xs, ys, zs]]
    if any(m is not np.ma.nomask for m in masks):
        combined = np.ma.mask_or(np.ma.mask_or(masks[0], masks[1]), masks[2])
        xs_scaled = np.ma.array(xs_scaled, mask=combined)
        ys_scaled = np.ma.array(ys_scaled, mask=combined)
        zs_scaled = np.ma.array(zs_scaled, mask=combined)

    return xs_scaled, ys_scaled, zs_scaled

