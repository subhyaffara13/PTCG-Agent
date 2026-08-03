import random

def test_broadcast_size_scalar():
    mu = np.ones(3)
    sigma = np.ones(3)
    random.normal(mu, sigma, size=3)
    with pytest.raises(ValueError):
        random.normal(mu, sigma, size=2)

