
def test_classify_ode():
    assert classify_ode(f(x).diff(x, 2), f(x)) == \
        (
        'nth_algebraic',
        'nth_linear_constant_coeff_homogeneous',
        'nth_linear_euler_eq_homogeneous',
        'Liouville',
        '2nd_power_series_ordinary',
        'nth_algebraic_Integral',
        'Liouville_Integral',
        )
    assert classify_ode(f(x), f(x)) == ('nth_algebraic', 'nth_algebraic_Integral')
    assert classify_ode(Eq(f(x).diff(x), 0), f(x)) == (
        'nth_algebraic',
        'separable',
        '1st_exact',
        '1st_linear',
        'Bernoulli',
        '1st_homogeneous_coeff_best',
        '1st_homogeneous_coeff_subs_indep_div_dep',
        '1st_homogeneous_coeff_subs_dep_div_indep',
        '1st_power_series', 'lie_group',
        'nth_linear_constant_coeff_homogeneous',
        'nth_linear_euler_eq_homogeneous',
        'nth_algebraic_Integral',
        'separable_Integral',
        '1st_exact_Integral',
        '1st_linear_Integral',
        'Bernoulli_Integral',
        '1st_homogeneous_coeff_subs_indep_div_dep_Integral',
        '1st_homogeneous_coeff_subs_dep_div_indep_Integral')
    assert classify_ode(f(x).diff(x)**2, f(x)) == ('factorable',
         'nth_algebraic',
         'separable',
         '1st_exact',
         '1st_linear',
         'Bernoulli',
         '1st_homogeneous_coeff_best',
         '1st_homogeneous_coeff_subs_indep_div_dep',
         '1st_homogeneous_coeff_subs_dep_div_indep',
         '1st_power_series',
         'lie_group',
         'nth_linear_euler_eq_homogeneous',
         'nth_algebraic_Integral',
         'separable_Integral',
         '1st_exact_Integral',
         '1st_linear_Integral',
         'Bernoulli_Integral',
         '1st_homogeneous_coeff_subs_indep_div_dep_Integral',
         '1st_homogeneous_coeff_subs_dep_div_indep_Integral')
    # issue 4749: f(x) should be cleared from highest derivative before classifying
    a = classify_ode(Eq(f(x).diff(x) + f(x), x), f(x))
    b = classify_ode(f(x).diff(x)*f(x) + f(x)*f(x) - x*f(x), f(x))
    c = classify_ode(f(x).diff(x)/f(x) + f(x)/f(x) - x/f(x), f(x))
    assert a == ('1st_exact',
        '1st_linear',
        'Bernoulli',
        'almost_linear',
        '1st_power_series', "lie_group",
        'nth_linear_constant_coeff_undetermined_coefficients',
        'nth_linear_constant_coeff_variation_of_parameters',
        '1st_exact_Integral',
        '1st_linear_Integral',
        'Bernoulli_Integral',
        'almost_linear_Integral',
        'nth_linear_constant_coeff_variation_of_parameters_Integral')
    assert b == ('factorable',
         '1st_linear',
         'Bernoulli',
         '1st_power_series',
         'lie_group',
         'nth_linear_constant_coeff_undetermined_coefficients',
         'nth_linear_constant_coeff_variation_of_parameters',
         '1st_linear_Integral',
         'Bernoulli_Integral',
         'nth_linear_constant_coeff_variation_of_parameters_Integral')
    assert c == ('factorable',
         '1st_linear',
         'Bernoulli',
         '1st_power_series',
         'lie_group',
         'nth_linear_constant_coeff_undetermined_coefficients',
         'nth_linear_constant_coeff_variation_of_parameters',
         '1st_linear_Integral',
         'Bernoulli_Integral',
         'nth_linear_constant_coeff_variation_of_parameters_Integral')

    assert classify_ode(
        2*x*f(x)*f(x).diff(x) + (1 + x)*f(x)**2 - exp(x), f(x)
    ) == ('factorable', '1st_exact', 'Bernoulli', 'almost_linear', 'lie_group',
        '1st_exact_Integral', 'Bernoulli_Integral', 'almost_linear_Integral')
    assert 'Riccati_special_minus2' in \
        classify_ode(2*f(x).diff(x) + f(x)**2 - f(x)/x + 3*x**(-2), f(x))
    raises(ValueError, lambda: classify_ode(x + f(x, y).diff(x).diff(
        y), f(x, y)))
    # issue 5176
    k = Symbol('k')
    assert classify_ode(f(x).diff(x)/(k*f(x) + k*x*f(x)) + 2*f(x)/(k*f(x) +
        k*x*f(x)) + x*f(x).diff(x)/(k*f(x) + k*x*f(x)) + z, f(x)) == \
        ('factorable', 'separable', '1st_exact', '1st_linear', 'Bernoulli',
        '1st_power_series', 'lie_group', 'separable_Integral', '1st_exact_Integral',
        '1st_linear_Integral', 'Bernoulli_Integral')
    # preprocessing
    ans = ('factorable', 'nth_algebraic', 'separable', '1st_exact', '1st_linear', 'Bernoulli',
        '1st_homogeneous_coeff_best',
        '1st_homogeneous_coeff_subs_indep_div_dep',
        '1st_homogeneous_coeff_subs_dep_div_indep',
        '1st_power_series', 'lie_group',
        'nth_linear_constant_coeff_undetermined_coefficients',
        'nth_linear_euler_eq_nonhomogeneous_undetermined_coefficients',
        'nth_linear_constant_coeff_variation_of_parameters',
        'nth_linear_euler_eq_nonhomogeneous_variation_of_parameters',
        'nth_algebraic_Integral',
        'separable_Integral', '1st_exact_Integral',
        '1st_linear_Integral',
        'Bernoulli_Integral',
        '1st_homogeneous_coeff_subs_indep_div_dep_Integral',
        '1st_homogeneous_coeff_subs_dep_div_indep_Integral',
        'nth_linear_constant_coeff_variation_of_parameters_Integral',
        'nth_linear_euler_eq_nonhomogeneous_variation_of_parameters_Integral')
    #     w/o f(x) given
    assert classify_ode(diff(f(x) + x, x) + diff(f(x), x)) == ans
    #     w/ f(x) and prep=True
    assert classify_ode(diff(f(x) + x, x) + diff(f(x), x), f(x),
                        prep=True) == ans

    assert classify_ode(Eq(2*x**3*f(x).diff(x), 0), f(x)) == \
        ('factorable', 'nth_algebraic', 'separable', '1st_exact',
         '1st_linear', 'Bernoulli', '1st_power_series',
         'lie_group', 'nth_linear_euler_eq_homogeneous',
         'nth_algebraic_Integral', 'separable_Integral', '1st_exact_Integral',
         '1st_linear_Integral', 'Bernoulli_Integral')


    assert classify_ode(Eq(2*f(x)**3*f(x).diff(x), 0), f(x)) == \
        ('factorable', 'nth_algebraic', 'separable', '1st_exact', '1st_linear',
         'Bernoulli', '1st_power_series', 'lie_group', 'nth_algebraic_Integral',
         'separable_Integral', '1st_exact_Integral', '1st_linear_Integral',
         'Bernoulli_Integral')
    # test issue 13864
    assert classify_ode(Eq(diff(f(x), x) - f(x)**x, 0), f(x)) == \
        ('1st_power_series', 'lie_group')
    assert isinstance(classify_ode(Eq(f(x), 5), f(x), dict=True), dict)

    #This is for new behavior of classify_ode when called internally with default, It should
    # return the first hint which matches therefore, 'ordered_hints' key will not be there.
    assert sorted(classify_ode(Eq(f(x).diff(x), 0), f(x), dict=True).keys()) == \
        ['default', 'nth_linear_constant_coeff_homogeneous', 'order']
    a = classify_ode(2*x*f(x)*f(x).diff(x) + (1 + x)*f(x)**2 - exp(x), f(x), dict=True, hint='Bernoulli')
    assert sorted(a.keys()) == ['Bernoulli', 'Bernoulli_Integral', 'default', 'order', 'ordered_hints']

    # test issue 22155
    a = classify_ode(f(x).diff(x) - exp(f(x) - x), f(x))
    assert a == ('separable',
        '1st_exact', '1st_power_series',
        'lie_group', 'separable_Integral',
        '1st_exact_Integral')

