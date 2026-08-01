
def _make_distribution_rv_generic(dist):
    parameters = []
    names = []
    support = getattr(dist, '_support', (dist.a, dist.b))
    for shape_info in dist._shape_info():
        domain = _RealInterval(endpoints=shape_info.endpoints,
                               inclusive=shape_info.inclusive)
        param = _RealParameter(shape_info.name, domain=domain)
        parameters.append(param)
        names.append(shape_info.name)

    repr_str = _distribution_names.get(dist.name, dist.name.capitalize())
    if isinstance(dist, stats.rv_continuous):
        old_class, new_class = stats.rv_continuous, ContinuousDistribution
    else:
        old_class, new_class = stats.rv_discrete, DiscreteDistribution

    def _overrides(method_name):
        return (getattr(dist.__class__, method_name, None)
                is not getattr(old_class, method_name, None))

    if _overrides("_get_support"):
        def left(**parameter_values):
            a, _ = dist._get_support(**parameter_values)
            return np.asarray(a)[()]

        def right(**parameter_values):
            _, b = dist._get_support(**parameter_values)
            return np.asarray(b)[()]

        endpoints = (left, right)
    else:
        endpoints = support

    _x_support = _RealInterval(endpoints=endpoints, inclusive=(True, True))
    _x_param = _RealParameter('x', domain=_x_support, typical=(-1, 1))

    class CustomDistribution(new_class):
        _parameterizations = ([_Parameterization(*parameters)] if parameters
                              else [])
        _variable = _x_param

        __class_getitem__ = None

        def __repr__(self):
            s = super().__repr__()
            return s.replace('CustomDistribution', repr_str)

        def __str__(self):
            s = super().__str__()
            return s.replace('CustomDistribution', repr_str)

    def _sample_formula(self, full_shape=(), *, rng=None, **kwargs):
        return dist._rvs(size=full_shape, random_state=rng, **kwargs)

    def _moment_raw_formula(self, order, **kwargs):
        return dist._munp(int(order), **kwargs)

    def _moment_raw_formula_1(self, order, **kwargs):
        if order != 1:
            return None
        return dist._stats(**kwargs)[0]

    def _moment_central_formula(self, order, **kwargs):
        if order != 2:
            return None
        return dist._stats(**kwargs)[1]

    def _moment_standard_formula(self, order, **kwargs):
        if order == 3:
            if dist._stats_has_moments:
                kwargs['moments'] = 's'
            return dist._stats(**kwargs)[int(order - 1)]
        elif order == 4:
            if dist._stats_has_moments:
                kwargs['moments'] = 'k'
            k = dist._stats(**kwargs)[int(order - 1)]
            return k if k is None else k + 3
        else:
            return None

    methods = {'_logpdf': '_logpdf_formula',
               '_pdf': '_pdf_formula',
               '_logpmf': '_logpmf_formula',
               '_pmf': '_pmf_formula',
               '_logcdf': '_logcdf_formula',
               '_cdf': '_cdf_formula',
               '_logsf': '_logccdf_formula',
               '_sf': '_ccdf_formula',
               '_ppf': '_icdf_formula',
               '_isf': '_iccdf_formula',
               '_entropy': '_entropy_formula',
               '_median': '_median_formula'}

    # These are not desirable overrides for the new infrastructure
    skip_override = {'norminvgauss': {'_sf', '_isf'}}

    for old_method, new_method in methods.items():
        if dist.name in skip_override and old_method in skip_override[dist.name]:
            continue
        # If method of old distribution overrides generic implementation...
        method = getattr(dist.__class__, old_method, None)
        super_method = getattr(old_class, old_method, None)
        if method is not super_method:
            # Make it an attribute of the new object with the new name
            setattr(CustomDistribution, new_method, getattr(dist, old_method))

    if _overrides('_munp'):
        CustomDistribution._moment_raw_formula = _moment_raw_formula

    if _overrides('_rvs'):
        CustomDistribution._sample_formula = _sample_formula

    if _overrides('_stats'):
        CustomDistribution._moment_standardized_formula = _moment_standard_formula
        if not _overrides('_munp'):
            CustomDistribution._moment_raw_formula = _moment_raw_formula_1
            CustomDistribution._moment_central_formula = _moment_central_formula

    support_etc = _combine_docs(CustomDistribution, include_examples=False).lstrip()
    docs = [
        f"This class represents `scipy.stats.{dist.name}` as a subclass of "
        f"`{new_class}`.",
        f"The `repr`/`str` of class instances is `{repr_str}`.",
        f"The PDF of the distribution is defined {support_etc}"
    ]
    CustomDistribution.__doc__ = ("\n".join(docs))

    return CustomDistribution

