
def test_X17():
    # Power series (compute the general formula)
    # (c41) powerseries(log(sin(x)/x), x, 0);
    # /aquarius/data2/opt/local/macsyma_422/library1/trgred.so being loaded.
    #              inf
    #              ====     i1  2 i1          2 i1
    #              \        (- 1)   2      bern(2 i1) x
    # (d41)         >        ------------------------------
    #              /             2 i1 (2 i1)!
    #              ====
    #              i1 = 1
    # fps does not calculate
    assert fps(log(sin(x)/x)) == \
        Sum((-1)**k*2**(2*k - 1)*bernoulli(2*k)*x**(2*k)/(k*factorial(2*k)), (k, 1, oo))

