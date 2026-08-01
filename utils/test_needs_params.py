
def test_needs_params(xp):
    for winstr in ['kaiser', 'ksr', 'kaiser_bessel_derived', 'kbd',
                   'gaussian', 'gauss', 'gss',
                   'general gaussian', 'general_gaussian',
                   'general gauss', 'general_gauss', 'ggs',
                   'dss', 'dpss', 'general cosine', 'general_cosine',
                   'chebwin', 'cheb', 'general hamming', 'general_hamming',
                   ]:
        assert_raises(ValueError, get_window, winstr, 7, xp=xp)

