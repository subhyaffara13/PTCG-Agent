
def test_setting_loc_scale():
    rng = FastGeneratorInversion(stats.norm(), random_state=765765864)
    r1 = rng.rvs(size=1000)
    rng.loc = 3.0
    rng.scale = 2.5
    r2 = rng.rvs(1000)
    # rescaled r2 should be again standard normal
    assert stats.cramervonmises_2samp(r1, (r2 - 3) / 2.5).pvalue > 0.05
    # reset values to default loc=0, scale=1
    rng.loc = 0
    rng.scale = 1
    r2 = rng.rvs(1000)
    assert stats.cramervonmises_2samp(r1, r2).pvalue > 0.05

