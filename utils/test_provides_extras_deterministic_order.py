
def test_provides_extras_deterministic_order():
    attrs = dict(extras_require=dict(a=['foo'], b=['bar']))
    dist = Distribution(attrs)
    assert list(dist.metadata.provides_extras) == ['a', 'b']
    attrs['extras_require'] = dict(reversed(attrs['extras_require'].items()))
    dist = Distribution(attrs)
    assert list(dist.metadata.provides_extras) == ['b', 'a']

