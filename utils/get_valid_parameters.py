
def get_valid_parameters(dist):
    # Given a distribution, return a logical array that is true where all
    # distribution parameters are within their respective domains. The code
    # here is probably quite similar to that used to form the `_invalid`
    # attribute of the distribution, but this was written about a week later
    # without referring to that code, so it is a somewhat independent check.

    # Get all parameter values and `_Parameter` objects
    parameter_values = dist._parameters
    parameters = {}
    for parameterization in dist._parameterizations:
        parameters.update(parameterization.parameters)

    all_valid = np.ones(dist._shape, dtype=bool)
    for name, value in parameter_values.items():
        if name not in parameters:  # cached value not part of parameterization
            continue
        parameter = parameters[name]

        # Check that the numerical endpoints and inclusivity attribute
        # agree with the `contains` method about which parameter values are
        # within the domain.
        a, b = parameter.domain.get_numerical_endpoints(
            parameter_values=parameter_values)
        a_included, b_included = parameter.domain.inclusive
        valid = (a <= value) if a_included else a < value
        valid &= (value <= b) if b_included else value < b
        assert_equal(valid, parameter.domain.contains(
            value, parameter_values=parameter_values))

        # Form `all_valid` mask that is True where *all* parameters are valid
        all_valid &= valid

    # Check that the `all_valid` mask formed here is the complement of the
    # `dist._invalid` mask stored by the infrastructure
    assert_equal(~all_valid, dist._invalid)

    return all_valid

