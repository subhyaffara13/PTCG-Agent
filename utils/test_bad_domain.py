
def test_bad_domain(domain, err, msg, method, kwargs):
    Method = getattr(stats.sampling, method)
    with pytest.raises(err, match=msg):
        Method(**kwargs, domain=domain)

