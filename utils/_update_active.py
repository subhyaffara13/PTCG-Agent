
def _update_active(work, res, res_work_pairs, active, mask, preserve_shape, xp):
    # Update `active` indices of the arrays in result object `res` with the
    # contents of the scalars and arrays in `update_dict`. When provided,
    # `mask` is a boolean array applied both to the arrays in `update_dict`
    # that are to be used and to the arrays in `res` that are to be updated.
    update_dict = {key1: work[key2] for key1, key2 in res_work_pairs}
    update_dict['success'] = work.status == 0

    if mask is not None:
        if preserve_shape:
            active_mask = xp.zeros_like(mask)
            active_mask = xpx.at(active_mask)[active].set(True)
            active_mask = active_mask & mask
            for key, val in update_dict.items():
                val = val[active_mask] if getattr(val, 'ndim', 0) > 0 else val
                res[key] = xpx.at(res[key])[active_mask].set(val)
        else:
            active_mask = active[mask]
            for key, val in update_dict.items():
                val = val[mask] if getattr(val, 'ndim', 0) > 0 else val
                res[key] = xpx.at(res[key])[active_mask].set(val)
    else:
        for key, val in update_dict.items():
            if preserve_shape and getattr(val, 'ndim', 0) > 0:
                val = val[active]
            res[key] = xpx.at(res[key])[active].set(val)

