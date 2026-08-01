
def test_warning_calls_filters(warning_calls):
    bad_filters, bad_stacklevels = warning_calls

    # We try not to add filters in the code base, because those filters aren't
    # thread-safe. We aim to only filter in tests with
    # warnings.catch_warnings. However, in some cases it may prove
    # necessary to filter out warnings, because we can't (easily) fix the root
    # cause for them and we don't want users to see some warnings when they use
    # SciPy correctly. So we list exceptions here.  Add new entries only if
    # there's a good reason.
    allowed_filters = (
        os.path.join('datasets', '_fetchers.py'),
        os.path.join('datasets', '__init__.py'),
        os.path.join('optimize', '_optimize.py'),
        os.path.join('optimize', '_constraints.py'),
        os.path.join('optimize', '_nnls.py'),
        os.path.join('signal', '_ltisys.py'),
        os.path.join('sparse', '__init__.py'),  # np.matrix pending-deprecation
        os.path.join('special', '_basic.py'),  # gh-21801
        os.path.join('stats', '_discrete_distns.py'),  # gh-14901
        os.path.join('stats', '_continuous_distns.py'),
        os.path.join('stats', '_binned_statistic.py'),  # gh-19345
        os.path.join('stats', '_stats_py.py'),  # gh-20743
        os.path.join('stats', '_variation.py'),  # gh-22827
        os.path.join('stats', 'tests', 'test_axis_nan_policy.py'),  # gh-20694
        os.path.join('_lib', '_util.py'),  # gh-19341
        os.path.join('sparse', 'linalg', '_dsolve', 'linsolve.py'),  # gh-17924
        "conftest.py",
    )
    bad_filters = [item for item in bad_filters if item.split(':')[0] not in
                   allowed_filters]

    if bad_filters:
        raise AssertionError(
            "Warning ignore filters should not be used outside of tests.\n"
            "Found in:\n    {}".format(
                "\n    ".join(bad_filters)))

