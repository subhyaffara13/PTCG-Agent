import random

def test_multinomial_1d_pval():
    # gh-20483
    with pytest.raises(TypeError, match="pvals must be a 1-d"):
        random.multinomial(10, 0.3)

