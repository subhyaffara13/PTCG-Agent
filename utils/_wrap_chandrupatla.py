
def _wrap_chandrupatla(func):
    def _chandrupatla_wrapper(f, *bracket, **kwargs):
        # avoid passing arguments to `find_minimum` to this function
        tol_keys = {'xatol', 'xrtol', 'fatol', 'frtol'}
        tolerances = {key: kwargs.pop(key) for key in tol_keys if key in kwargs}
        _callback = kwargs.pop('callback', None)
        if callable(_callback):
            def callback(res):
                if func == find_root:
                    res.xl, res.xr = res.bracket
                    res.fl, res.fr = res.f_bracket
                else:
                    res.xl, res.xm, res.xr = res.bracket
                    res.fl, res.fm, res.fr = res.f_bracket
                res.fun = res.f_x
                del res.bracket
                del res.f_bracket
                del res.f_x
                return _callback(res)
        else:
            callback = _callback

        res = func(f, bracket, tolerances=tolerances, callback=callback, **kwargs)
        if func == find_root:
            res.xl, res.xr = res.bracket
            res.fl, res.fr = res.f_bracket
        else:
            res.xl, res.xm, res.xr = res.bracket
            res.fl, res.fm, res.fr = res.f_bracket
        res.fun = res.f_x
        del res.bracket
        del res.f_bracket
        del res.f_x
        return res
    return _chandrupatla_wrapper

