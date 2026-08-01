
def test_hist_vectorized_params(fig_test, fig_ref, kwargs):
    np.random.seed(19680801)
    xs = [np.random.randn(n) for n in [20, 50, 100]]

    (axt1, axt2) = fig_test.subplots(2)
    (axr1, axr2) = fig_ref.subplots(2)

    for histtype, axt, axr in [("stepfilled", axt1, axr1), ("step", axt2, axr2)]:
        _, bins, _ = axt.hist(xs, bins=10, histtype=histtype, **kwargs)

        kw, values = next(iter(kwargs.items()))
        for i, (x, value) in enumerate(zip(xs, values)):
            axr.hist(x, bins=bins, histtype=histtype, **{kw: value},
                     zorder=(len(xs)-i)/2)

