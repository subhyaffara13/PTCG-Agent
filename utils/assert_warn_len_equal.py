
def assert_warn_len_equal(mod, n_in_context):
    try:
        mod_warns = mod.__warningregistry__
    except AttributeError:
        # the lack of a __warningregistry__
        # attribute means that no warning has
        # occurred; this can be triggered in
        # a parallel test scenario, while in
        # a serial test scenario an initial
        # warning (and therefore the attribute)
        # are always created first
        mod_warns = {}

    num_warns = len(mod_warns)

    if 'version' in mod_warns:
        # Python adds a 'version' entry to the registry,
        # do not count it.
        num_warns -= 1

    assert_equal(num_warns, n_in_context)

