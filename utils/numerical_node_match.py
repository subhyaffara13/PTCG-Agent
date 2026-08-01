
def numerical_node_match(attr, default, rtol=1.0000000000000001e-05, atol=1e-08):
    if isinstance(attr, str):

        def match(data1, data2):
            return math.isclose(
                data1.get(attr, default),
                data2.get(attr, default),
                rel_tol=rtol,
                abs_tol=atol,
            )

    else:
        attrs = list(zip(attr, default))  # Python 3

        def match(data1, data2):
            values1 = [data1.get(attr, d) for attr, d in attrs]
            values2 = [data2.get(attr, d) for attr, d in attrs]
            return allclose(values1, values2, rtol=rtol, atol=atol)

    return match

