
def _make_distribution_custom(dist):
    dist_parameters = (
        dist.parameters if isinstance(dist.parameters, tuple) else (dist.parameters, )
    )
    parameterizations = []
    for parameterization in dist_parameters:
        # The attribute name ``parameters`` appears reasonable from a user facing
        # perspective, but there is a little tension here with the internal. It's
        # important to keep in mind that the ``parameters`` attribute in a
        # user-created custom distribution specifies ``_parameterizations`` within
        # the infrastructure.
        parameters = []

        for name, info in parameterization.items():
            domain_info, typical = _get_domain_info(info)
            domain = _RealInterval(**domain_info)
            param = _RealParameter(name, domain=domain, typical=typical)
            parameters.append(param)

        if parameters:
            parameterizations.append(_Parameterization(*parameters))

    domain_info, typical = _get_domain_info(dist.support)
    _x_support = _RealInterval(**domain_info)
    _x_param = _RealParameter('x', domain=_x_support, typical=typical)
    repr_str = dist.__class__.__name__

    class CustomDistribution(ContinuousDistribution):
        _parameterizations = parameterizations
        _variable = _x_param

        def __repr__(self):
            s = super().__repr__()
            return s.replace('CustomDistribution', repr_str)

        def __str__(self):
            s = super().__str__()
            return s.replace('CustomDistribution', repr_str)

    methods = {'sample', 'logentropy', 'entropy',
               'median', 'mode', 'logpdf', 'pdf',
               'logcdf2', 'logcdf', 'cdf2', 'cdf',
               'logccdf2', 'logccdf', 'ccdf2', 'ccdf',
               'ilogcdf', 'icdf', 'ilogccdf', 'iccdf',
               'lmoment'}

    for method in methods:
        if hasattr(dist, method):
            # Make it an attribute of the new object with the new name
            new_method = f"_{method}_formula"
            setattr(CustomDistribution, new_method, getattr(dist, method))

    if hasattr(dist, 'moment'):
        def _moment_raw_formula(self, order, **kwargs):
            return dist.moment(order, kind='raw', **kwargs)

        def _moment_central_formula(self, order, **kwargs):
            return dist.moment(order, kind='central', **kwargs)

        def _moment_standardized_formula(self, order, **kwargs):
            return dist.moment(order, kind='standardized', **kwargs)

        CustomDistribution._moment_raw_formula = _moment_raw_formula
        CustomDistribution._moment_central_formula = _moment_central_formula
        CustomDistribution._moment_standardized_formula = _moment_standardized_formula

    if hasattr(dist, 'process_parameters'):
        setattr(
            CustomDistribution,
            "_process_parameters",
            getattr(dist, "process_parameters")
        )

    support_etc = _combine_docs(CustomDistribution, include_examples=False).lstrip()
    docs = [
        f"This class represents `{repr_str}` as a subclass of "
        "`ContinuousDistribution`.",
        f"The PDF of the distribution is defined {support_etc}"
    ]
    CustomDistribution.__doc__ = ("\n".join(docs))

    return CustomDistribution

