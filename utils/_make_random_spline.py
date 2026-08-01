
def _make_random_spline(n=35, k=3, xp=np):
    rng = np.random.RandomState(123)
    t = np.sort(rng.random(n+k+1))
    c = rng.random(n)
    t, c = xp.asarray(t), xp.asarray(c)
    return BSpline.construct_fast(t, c, k)

