
def _prepare_result(work, res, res_work_pairs, active, shape, customize_result,
                    preserve_shape, xp):
    # Prepare the result object `res` by creating a copy, copying the latest
    # data from work, running the provided result customization function,
    # and reshaping the data to the original shapes.
    res = res.copy()
    _update_active(work, res, res_work_pairs, active, None, preserve_shape, xp)

    shape = customize_result(res, shape)

    for key, val in res.items():
        # this looks like it won't work for xp != np if val is not numeric
        temp = xp.reshape(val, shape)
        res[key] = temp[()] if temp.ndim == 0 else temp

    res['_order_keys'] = ['success'] + [i for i, j in res_work_pairs]
    return _RichResult(**res)

