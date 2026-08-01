
def test_median_cihs():
    # Basic test against R library EnvStats function `eqnpar`, e.g.
    # library(EnvStats)
    # options(digits=8)
    # x = c(0.88612955, 0.35242375, 0.66240904, 0.94617974, 0.10929913,
    #       0.76699506, 0.88550655, 0.62763754, 0.76818588, 0.68506508,
    #       0.88043148, 0.03911248, 0.93805564, 0.95326961, 0.25291112,
    #       0.16128487, 0.49784577, 0.24588924, 0.6597, 0.92239679)
    # eqnpar(x, p=0.5,
    #        ci.method = "interpolate", approx.conf.level = 0.95, ci = TRUE)
    rng = np.random.default_rng(8824288259505800535)
    x = rng.random(size=20)
    assert_allclose(ms.median_cihs(x), (0.38663198, 0.88431272))

    # SciPy's 90% CI upper limit doesn't match that of EnvStats eqnpar. SciPy
    # doesn't look wrong, and it agrees with a different reference,
    # `median_confint_hs` from `hoehleatsu/quantileCI`.
    # In (e.g.) Colab with R runtime:
    # devtools::install_github("hoehleatsu/quantileCI")
    # library(quantileCI)
    # median_confint_hs(x=x, conf.level=0.90, interpolate=TRUE)
    assert_allclose(ms.median_cihs(x, 0.1), (0.48319773366, 0.88094268050))

