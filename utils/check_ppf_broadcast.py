
def check_ppf_broadcast(distfn, arg, msg):
    # compares ppf for multiple argsets.
    num_repeats = 5
    args = [] * num_repeats
    if arg:
        args = [np.array([_] * num_repeats) for _ in arg]

    median = distfn.ppf(0.5, *arg)
    medians = distfn.ppf(0.5, *args)
    msg += " - ppf multiple"
    npt.assert_almost_equal(medians, [median] * num_repeats, decimal=7, err_msg=msg)

