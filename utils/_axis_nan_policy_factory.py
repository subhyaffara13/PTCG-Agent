
def _axis_nan_policy_factory(tuple_to_result, default_axis=0,
                             n_samples=1, paired=False,
                             result_to_tuple=None, too_small=0,
                             n_outputs=2, kwd_samples=(), override=None):
    """Factory for a wrapper that adds axis/nan_policy params to a function.

    Parameters
    ----------
    tuple_to_result : callable
        Callable that returns an object of the type returned by the function
        being wrapped (e.g. the namedtuple or dataclass returned by a
        statistical test) provided the separate components (e.g. statistic,
        pvalue).
    default_axis : int, default: 0
        The default value of the axis argument. Standard is 0 except when
        backwards compatibility demands otherwise (e.g. `None`).
    n_samples : int or callable, default: 1
        The number of data samples accepted by the function
        (e.g. `mannwhitneyu`), a callable that accepts a dictionary of
        parameters passed into the function and returns the number of data
        samples (e.g. `wilcoxon`), or `None` to indicate an arbitrary number
        of samples (e.g. `kruskal`).
    paired : {False, True}
        Whether the function being wrapped treats the samples as paired (i.e.
        corresponding elements of each sample should be considered as different
        components of the same sample.)
    result_to_tuple : callable, optional
        Function that unpacks the results of the function being wrapped into
        a tuple. This is essentially the inverse of `tuple_to_result`. Default
        is `None`, which is appropriate for statistical tests that return a
        statistic, pvalue tuple (rather than, e.g., a non-iterable dataclass).
    too_small : int or callable, default: 0
        The largest unacceptably small sample for the function being wrapped.
        For example, some functions require samples of size two or more or they
        raise an error. This argument prevents the error from being raised when
        input is not 1D and instead places a NaN in the corresponding element
        of the result. If callable, it must accept a list of samples, axis,
        and a dictionary of keyword arguments passed to the wrapper function as
        arguments and return a bool indicating whether the samples passed are
        too small.
    n_outputs : int or callable, default: 2
        The number of outputs produced by the function given 1d sample(s). For
        example, hypothesis tests that return a namedtuple or result object
        with attributes ``statistic`` and ``pvalue`` use the default
        ``n_outputs=2``; summary statistics with scalar output use
        ``n_outputs=1``. Alternatively, may be a callable that accepts a
        dictionary of arguments passed into the wrapped function and returns
        the number of outputs corresponding with those arguments.
    kwd_samples : sequence, default: ()
        The names of keyword parameters that should be treated as samples. For
        example, `gmean` accepts as its first argument a sample `a` but
        also `weights` as a fourth, optional keyword argument. In this case, we
        use `n_samples=1` and kwd_samples=['weights'].
    override : dict, default: {'vectorization': False, 'nan_propagation': True}
        Pass a dictionary with ``'vectorization': True`` to ensure that the
        decorator overrides the function's behavior for multimensional input.
        Use ``'nan_propagation': False`` to ensure that the decorator does not
        override the function's behavior for ``nan_policy='propagate'``.
    """
    # Specify which existing behaviors the decorator must override
    temp = override or {}
    override = {'vectorization': False,
                'nan_propagation': True}
    override.update(temp)

    if result_to_tuple is None:
        def result_to_tuple(res, _):
            return res

    if not callable(too_small):
        def is_too_small(samples, *ts_args, axis=-1, **ts_kwargs):
            for sample in samples:
                if sample.shape[axis] <= too_small:
                    return True
            return False
    else:
        is_too_small = too_small

    def axis_nan_policy_decorator(hypotest_fun_in):
        @wraps(hypotest_fun_in)
        def axis_nan_policy_wrapper(*args, _no_deco=False, **kwds):

            if _no_deco:  # for testing, decorator does nothing
                return hypotest_fun_in(*args, **kwds)

            # For now, skip the decorator entirely if using array API. In the future,
            # we'll probably want to use it for `keepdims`, `axis` tuples, etc.
            if len(args) == 0:  # extract sample from `kwds` if there are no `args`
                used_kwd_samples = list(set(kwds).intersection(set(kwd_samples)))
                temp = used_kwd_samples[:1]
            else:
                temp = args[0]

            if is_dask(array_namespace(temp)):
                msg = ("Use of `nan_policy` and `keepdims` "
                       "is incompatible with lazy arrays.")
                if 'nan_policy' in kwds or 'keepdims' in kwds:
                    raise NotImplementedError(msg)
                return hypotest_fun_in(*args, **kwds)

            # We need to be flexible about whether position or keyword
            # arguments are used, but we need to make sure users don't pass
            # both for the same parameter. To complicate matters, some
            # functions accept samples with *args, and some functions already
            # accept `axis` and `nan_policy` as positional arguments.
            # The strategy is to make sure that there is no duplication
            # between `args` and `kwds`, combine the two into `kwds`, then
            # the samples, `nan_policy`, and `axis` from `kwds`, as they are
            # dealt with separately.

            # Check for intersection between positional and keyword args
            params = list(inspect.signature(hypotest_fun_in).parameters)
            if n_samples is None:
                # Give unique names to each positional sample argument
                # Note that *args can't be provided as a keyword argument
                params = [f"arg{i}" for i in range(len(args))] + params[1:]

            # raise if there are too many positional args
            maxarg = (np.inf if inspect.getfullargspec(hypotest_fun_in).varargs
                      else len(inspect.getfullargspec(hypotest_fun_in).args))
            if len(args) > maxarg:  # let the function raise the right error
                hypotest_fun_in(*args, **kwds)

            # raise if multiple values passed for same parameter
            d_args = dict(zip(params, args))
            intersection = set(d_args) & set(kwds)
            if intersection:  # let the function raise the right error
                hypotest_fun_in(*args, **kwds)

            # Consolidate other positional and keyword args into `kwds`
            kwds.update(d_args)

            # rename avoids UnboundLocalError
            if callable(n_samples):
                # Future refactoring idea: no need for callable n_samples.
                # Just replace `n_samples` and `kwd_samples` with a single
                # list of the names of all samples, and treat all of them
                # as `kwd_samples` are treated below.
                n_samp = n_samples(kwds)
            else:
                n_samp = n_samples or len(args)

            # get the number of outputs
            n_out = n_outputs  # rename to avoid UnboundLocalError
            if callable(n_out):
                n_out = n_out(kwds)

            # If necessary, rearrange function signature: accept other samples
            # as positional args right after the first n_samp args
            kwd_samp = [name for name in kwd_samples
                        if kwds.get(name, None) is not None]
            n_kwd_samp = len(kwd_samp)
            if not kwd_samp:
                hypotest_fun_out = hypotest_fun_in
            else:
                def hypotest_fun_out(*samples, **kwds):
                    new_kwds = dict(zip(kwd_samp, samples[n_samp:]))
                    kwds.update(new_kwds)
                    return hypotest_fun_in(*samples[:n_samp], **kwds)

            # Extract the things we need here
            try:  # if something is missing
                samples = [kwds.pop(param) for param in (params[:n_samp] + kwd_samp)]
                xp = array_namespace(*samples)
                samples = xp_promote(*samples, xp=xp)
                samples = (samples,) if not isinstance(samples, tuple) else samples
                samples = [xpx.atleast_nd(sample, ndim=1) for sample in samples]
            except KeyError:  # let the function raise the right error
                # might need to revisit this if required arg is not a "sample"
                hypotest_fun_in(*args, **kwds)
            vectorized = True if 'axis' in params else False
            vectorized = vectorized and not override['vectorization']
            axis = kwds.pop('axis', default_axis)
            nan_policy = kwds.pop('nan_policy', 'propagate')
            keepdims = kwds.pop("keepdims", False)
            del args  # avoid the possibility of passing both `args` and `kwds`

            # convert masked arrays to regular arrays with sentinel values
            sentinel = None
            if is_numpy(xp):
                samples, sentinel = _masked_arrays_2_sentinel_arrays(samples)

            # standardize to always work along last axis
            reduced_axes = axis
            if axis is None:
                if samples:
                    # when axis=None, take the maximum of all dimensions since
                    # all the dimensions are reduced.
                    n_dims = max([xp.asarray(sample).ndim for sample in samples])
                    reduced_axes = tuple(range(n_dims))
                samples = [xp_ravel(sample) for sample in samples]
            else:
                # don't ignore any axes when broadcasting if paired
                samples = _broadcast_arrays(samples, axis=axis if not paired else None)
                axis = (axis,) if np.isscalar(axis) else axis
                n_axes = len(axis)
                # move all axes in `axis` to the end to be raveled
                samples = [xp.moveaxis(sample, axis, tuple(range(-len(axis), 0)))
                           for sample in samples]
                shapes = [sample.shape for sample in samples]
                # New shape is unchanged for all axes _not_ in `axis`
                # At the end, we append the product of the shapes of the axes
                # in `axis`. Appending -1 doesn't work for zero-size arrays!
                new_shapes = [shape[:-n_axes] + (math.prod(shape[-n_axes:]),)
                              for shape in shapes]
                samples = [xp.reshape(sample, new_shape)
                           for sample, new_shape in zip(samples, new_shapes)]
            axis = -1  # work over the last axis

            NaN = _get_nan(*samples) if samples else xp.nan

            # if axis is not needed, just handle nan_policy and return
            ndims = np.array([sample.ndim for sample in samples])  # NumPy OK for ndims
            if np.all(ndims <= 1):
                # Addresses nan_policy == "raise"
                if nan_policy != 'propagate' or override['nan_propagation']:
                    contains_nan = [_contains_nan(sample, nan_policy)
                                    for sample in samples]
                else:
                    # Behave as though there are no NaNs (even if there are)
                    contains_nan = [False] * len(samples)

                # To give JAX most benefits of the `_axis_nan_policy` decorator without
                # value-dependent branching, the decorator will always treat JAX arrays
                # as if there are no NaNs. Typically, this means that NaNs will
                # multidimensional naturally. However, there may be cases in which this
                # doesn't produce the desired result, so for now, JAX users should
                # treat all functions as though there is no explicit`nan_policy`.
                # Future work tracked in gh-14651.
                any_contains_nan = not is_jax(xp) and any(contains_nan)
                # Addresses nan_policy == "propagate"
                if any_contains_nan and (nan_policy == 'propagate'
                                         and override['nan_propagation']):
                    res = xp.full(n_out, xp.nan, dtype=NaN.dtype)
                    res = _add_reduced_axes(res, reduced_axes, keepdims)
                    return tuple_to_result(*res)

                # Addresses nan_policy == "omit"
                too_small_msg = too_small_1d_not_omit
                if any_contains_nan and nan_policy == 'omit':
                    # consider passing in contains_nan
                    samples = _remove_nans(samples, paired)
                    too_small_msg = too_small_1d_omit

                if sentinel:
                    samples = _remove_sentinel(samples, paired, sentinel)

                if is_too_small(samples, kwds):
                    warnings.warn(too_small_msg, SmallSampleWarning, stacklevel=2)
                    res = xp.full(n_out, xp.nan, dtype=NaN.dtype)
                    res = _add_reduced_axes(res, reduced_axes, keepdims)
                    return tuple_to_result(*res)

                res = hypotest_fun_out(*samples, **kwds)
                res = result_to_tuple(res, n_out)
                res = _add_reduced_axes(res, reduced_axes, keepdims)
                return tuple_to_result(*res)

            # check for empty input
            empty_output = _check_empty_inputs(samples, axis, xp=xp)
            # only return empty output if zero sized input is too small.
            if (
                empty_output is not None
                and (is_too_small(samples, kwds) or xp_size(empty_output) == 0)
            ):
                if is_too_small(samples, kwds) and xp_size(empty_output) != 0:
                    warnings.warn(too_small_nd_not_omit, SmallSampleWarning,
                                  stacklevel=2)
                res = [xp_copy(empty_output) for i in range(n_out)]
                res = _add_reduced_axes(res, reduced_axes, keepdims)
                return tuple_to_result(*res)

            if not is_numpy(xp) and 'nan_policy' in kwds:
                msg = ("Use of `nan_policy` is incompatible with multidimensional "
                       "non-NumPy arrays.")
                raise NotImplementedError(msg)

            if not is_numpy(xp):
                res = hypotest_fun_out(*samples, axis=axis, **kwds)
                res = result_to_tuple(res, n_out)
                res = _add_reduced_axes(res, reduced_axes, keepdims, xp=xp)
                return tuple_to_result(*res)

            # otherwise, concatenate all samples along axis, remembering where
            # each separate sample begins
            lengths = np.array([sample.shape[axis] for sample in samples])
            split_indices = np.cumsum(lengths)
            x = _broadcast_concatenate(samples, axis, paired=paired)

            # Addresses nan_policy == "raise"
            if nan_policy != 'propagate' or override['nan_propagation']:
                contains_nan = _contains_nan(x, nan_policy)
            else:
                contains_nan = False  # behave like there are no NaNs

            if vectorized and not contains_nan and not sentinel:
                res = hypotest_fun_out(*samples, axis=axis, **kwds)
                res = result_to_tuple(res, n_out)
                res = _add_reduced_axes(res, reduced_axes, keepdims)
                return tuple_to_result(*res)

            # Addresses nan_policy == "omit"
            if contains_nan and nan_policy == 'omit':
                def hypotest_fun(x):
                    samples = np.split(x, split_indices)[:n_samp+n_kwd_samp]
                    samples = _remove_nans(samples, paired)
                    if sentinel:
                        samples = _remove_sentinel(samples, paired, sentinel)
                    if is_too_small(samples, kwds):
                        warnings.warn(too_small_nd_omit, SmallSampleWarning,
                                      stacklevel=4)
                        return np.full(n_out, NaN)
                    return result_to_tuple(hypotest_fun_out(*samples, **kwds), n_out)

            # Addresses nan_policy == "propagate"
            elif (contains_nan and nan_policy == 'propagate'
                  and override['nan_propagation']):
                def hypotest_fun(x):
                    if np.isnan(x).any():
                        return np.full(n_out, NaN)

                    samples = np.split(x, split_indices)[:n_samp+n_kwd_samp]
                    if sentinel:
                        samples = _remove_sentinel(samples, paired, sentinel)
                    if is_too_small(samples, kwds):
                        return np.full(n_out, NaN)
                    return result_to_tuple(hypotest_fun_out(*samples, **kwds), n_out)

            else:
                def hypotest_fun(x):
                    samples = np.split(x, split_indices)[:n_samp+n_kwd_samp]
                    if sentinel:
                        samples = _remove_sentinel(samples, paired, sentinel)
                    if is_too_small(samples, kwds):
                        return np.full(n_out, NaN)
                    return result_to_tuple(hypotest_fun_out(*samples, **kwds), n_out)

            x = np.moveaxis(x, axis, 0)
            res = np.apply_along_axis(hypotest_fun, axis=0, arr=x)
            res = _add_reduced_axes(res, reduced_axes, keepdims)
            return tuple_to_result(*res)

        _axis_parameter_doc, _axis_parameter = _get_axis_params(default_axis)
        doc = FunctionDoc(axis_nan_policy_wrapper)
        parameter_names = [param.name for param in doc['Parameters']]
        if 'axis' in parameter_names:
            doc['Parameters'][parameter_names.index('axis')] = (
                _axis_parameter_doc)
        else:
            doc['Parameters'].append(_axis_parameter_doc)
        if 'nan_policy' in parameter_names:
            doc['Parameters'][parameter_names.index('nan_policy')] = (
                _nan_policy_parameter_doc)
        else:
            doc['Parameters'].append(_nan_policy_parameter_doc)
        if 'keepdims' in parameter_names:
            doc['Parameters'][parameter_names.index('keepdims')] = (
                _keepdims_parameter_doc)
        else:
            doc['Parameters'].append(_keepdims_parameter_doc)
        doc['Notes'] += _standard_note_addition
        doc = str(doc).split("\n", 1)[1].lstrip(" \n")  # remove signature
        axis_nan_policy_wrapper.__doc__ = str(doc)

        sig = inspect.signature(axis_nan_policy_wrapper)
        parameters = sig.parameters
        parameter_list = list(parameters.values())
        if 'axis' not in parameters:
            parameter_list.append(_axis_parameter)
        if 'nan_policy' not in parameters:
            parameter_list.append(_nan_policy_parameter)
        if 'keepdims' not in parameters:
            parameter_list.append(_keepdims_parameter)
        sig = sig.replace(parameters=parameter_list)
        axis_nan_policy_wrapper.__signature__ = sig

        return axis_nan_policy_wrapper
    return axis_nan_policy_decorator

