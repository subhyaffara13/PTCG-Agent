
def _polynomial_integrate(polynomials, facets, hp_params):
    dims = (x, y)
    dim_length = len(dims)
    integral_value = S.Zero
    for deg in polynomials:
        poly_contribute = S.Zero
        facet_count = 0
        for hp in hp_params:
            value_over_boundary = integration_reduction(facets,
                                                        facet_count,
                                                        hp[0], hp[1],
                                                        polynomials[deg],
                                                        dims, deg)
            poly_contribute += value_over_boundary * (hp[1] / norm(hp[0]))
            facet_count += 1
        poly_contribute /= (dim_length + deg)
        integral_value += poly_contribute

    return integral_value

