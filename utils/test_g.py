
def test_g():
    # Test data for the g_k. See DLMF 5.11.4.
    with mp.workdps(30):
        g = [mp.mpf(1), mp.mpf(1)/12, mp.mpf(1)/288,
             -mp.mpf(139)/51840, -mp.mpf(571)/2488320,
             mp.mpf(163879)/209018880, mp.mpf(5246819)/75246796800]
        mp_assert_allclose(compute_g(7), g)

