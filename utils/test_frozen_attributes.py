
def test_frozen_attributes(monkeypatch):
    # gh-14827 reported that all frozen distributions had both pmf and pdf
    # attributes; continuous should have pdf and discrete should have pmf.
    message = "'rv_continuous_frozen' object has no attribute"
    with pytest.raises(AttributeError, match=message):
        stats.norm().pmf
    with pytest.raises(AttributeError, match=message):
        stats.norm().logpmf
    monkeypatch.setattr(stats.norm, "pmf", "herring", raising=False)
    frozen_norm = stats.norm()
    assert isinstance(frozen_norm, rv_continuous_frozen)
    assert not hasattr(frozen_norm, "pmf")


def test_frozen_attributes(monkeypatch):
    # gh-14827 reported that all frozen distributions had both pmf and pdf
    # attributes; continuous should have pdf and discrete should have pmf.
    message = "'rv_discrete_frozen' object has no attribute"
    with pytest.raises(AttributeError, match=message):
        stats.binom(10, 0.5).pdf
    with pytest.raises(AttributeError, match=message):
        stats.binom(10, 0.5).logpdf
    monkeypatch.setattr(stats.binom, "pdf", "herring", raising=False)
    frozen_binom = stats.binom(10, 0.5)
    assert isinstance(frozen_binom, rv_discrete_frozen)
    assert not hasattr(frozen_binom, "pdf")

