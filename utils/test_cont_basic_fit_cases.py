
def test_cont_basic_fit_cases():
    # Distribution names should not be in multiple MLE or MM sets
    assert (len(xslow_fit_mle.union(xfail_fit_mle).union(skip_fit_mle)) ==
            len(xslow_fit_mle) + len(xfail_fit_mle) + len(skip_fit_mle))
    assert (len(xslow_fit_mm.union(xfail_fit_mm).union(skip_fit_mm)) ==
            len(xslow_fit_mm) + len(xfail_fit_mm) + len(skip_fit_mm))

