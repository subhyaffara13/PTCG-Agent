
def test_definition():
    # want to test if the system can have several units of the same dimension
    dm = Quantity("dm")
    base = (m, s)
    # base_dim = (m.dimension, s.dimension)
    ms = UnitSystem(base, (c, dm), "MS", "MS system")
    ms.set_quantity_dimension(dm, length)
    ms.set_quantity_scale_factor(dm, Rational(1, 10))

    assert set(ms._base_units) == set(base)
    assert set(ms._units) == {m, s, c, dm}
    # assert ms._units == DimensionSystem._sort_dims(base + (velocity,))
    assert ms.name == "MS"
    assert ms.descr == "MS system"


def test_definition(fftwdata_size, rdt, type, reference_data, ref_lock):
    with ref_lock:
        xr, yr, dt = fftw_dst_ref(type, fftwdata_size, rdt, reference_data)
    y = dst(xr, type=type)
    dec = dec_map[(dst, rdt, type)]
    assert_equal(y.dtype, dt)
    assert_allclose(y, yr, rtol=0., atol=np.max(yr)*10**(-dec))

