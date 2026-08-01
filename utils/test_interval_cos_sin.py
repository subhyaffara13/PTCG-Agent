
def test_interval_cos_sin():
    iv.dps = 15
    cos = iv.cos
    sin = iv.sin
    tan = iv.tan
    pi = iv.pi
    # Around 0
    assert cos(mpi(0)) == 1
    assert sin(mpi(0)) == 0
    assert cos(mpi(0,1)) == mpi(0.54030230586813965399, 1.0)
    assert sin(mpi(0,1)) == mpi(0, 0.8414709848078966159)
    assert cos(mpi(1,2)) == mpi(-0.4161468365471424069, 0.54030230586813976501)
    assert sin(mpi(1,2)) == mpi(0.84147098480789650488, 1.0)
    assert sin(mpi(1,2.5)) == mpi(0.59847214410395643824, 1.0)
    assert cos(mpi(-1, 1)) == mpi(0.54030230586813965399, 1.0)
    assert cos(mpi(-1, 0.5)) == mpi(0.54030230586813965399, 1.0)
    assert cos(mpi(-1, 1.5)) == mpi(0.070737201667702906405, 1.0)
    assert sin(mpi(-1,1)) == mpi(-0.8414709848078966159, 0.8414709848078966159)
    assert sin(mpi(-1,0.5)) == mpi(-0.8414709848078966159, 0.47942553860420300538)
    assert mpi(-0.8414709848078966159, 1.00000000000000002e-100) in sin(mpi(-1,1e-100))
    assert mpi(-2.00000000000000004e-100, 1.00000000000000002e-100) in sin(mpi(-2e-100,1e-100))
    # Same interval
    assert cos(mpi(2, 2.5))
    assert cos(mpi(3.5, 4)) == mpi(-0.93645668729079634129, -0.65364362086361182946)
    assert cos(mpi(5, 5.5)) == mpi(0.28366218546322624627, 0.70866977429126010168)
    assert mpi(0.59847214410395654927, 0.90929742682568170942) in sin(mpi(2, 2.5))
    assert sin(mpi(3.5, 4)) == mpi(-0.75680249530792831347, -0.35078322768961983646)
    assert sin(mpi(5, 5.5)) == mpi(-0.95892427466313856499, -0.70554032557039181306)
    # Higher roots
    iv.dps = 55
    w = 4*10**50 + mpi(0.5)
    for p in [15, 40, 80]:
        iv.dps = p
        assert 0 in sin(4*mpi(pi))
        assert 0 in sin(4*10**50*mpi(pi))
        assert 0 in cos((4+0.5)*mpi(pi))
        assert 0 in cos(w*mpi(pi))
        assert 1 in cos(4*mpi(pi))
        assert 1 in cos(4*10**50*mpi(pi))
    iv.dps = 15
    assert cos(mpi(2,inf)) == mpi(-1,1)
    assert sin(mpi(2,inf)) == mpi(-1,1)
    assert cos(mpi(-inf,2)) == mpi(-1,1)
    assert sin(mpi(-inf,2)) == mpi(-1,1)
    u = tan(mpi(0.5,1))
    assert mpf(u.a).ae(mp.tan(0.5))
    assert mpf(u.b).ae(mp.tan(1))
    v = iv.cot(mpi(0.5,1))
    assert mpf(v.a).ae(mp.cot(1))
    assert mpf(v.b).ae(mp.cot(0.5))
    # Sanity check of evaluation at n*pi and (n+1/2)*pi
    for n in range(-5,7,2):
        x = iv.cos(n*iv.pi)
        assert -1 in x
        assert x >= -1
        assert x != -1
        x = iv.sin((n+0.5)*iv.pi)
        assert -1 in x
        assert x >= -1
        assert x != -1
    for n in range(-6,8,2):
        x = iv.cos(n*iv.pi)
        assert 1 in x
        assert x <= 1
        if n:
            assert x != 1
        x = iv.sin((n+0.5)*iv.pi)
        assert 1 in x
        assert x <= 1
        assert x != 1
    for n in range(-6,7):
        x = iv.cos((n+0.5)*iv.pi)
        assert x.a < 0 < x.b
        x = iv.sin(n*iv.pi)
        if n:
            assert x.a < 0 < x.b

