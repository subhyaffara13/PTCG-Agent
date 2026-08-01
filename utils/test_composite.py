
def test_composite():
    from sympy.ntheory.generate import sieve
    sieve._reset()
    assert composite(1) == 4
    assert composite(2) == 6
    assert composite(5) == 10
    assert composite(11) == 20
    assert composite(41) == 58
    assert composite(57) == 80
    assert composite(296) == 370
    assert composite(559) == 684
    assert composite(3000) == 3488
    assert composite(4096) == 4736
    assert composite(9096) == 10368
    assert composite(25023) == 28088
    sieve.extend(3000)
    assert composite(1957) == 2300
    assert composite(2568) == 2998
    raises(ValueError, lambda: composite(0))


def test_composite():
    assert S.NegativeOne.is_composite is False
    assert S(-2).is_composite is False
    assert S(-4).is_composite is False
    assert S.Zero.is_composite is False
    assert S(2).is_composite is False
    assert S(17).is_composite is False
    assert S(4).is_composite is True
    x = Dummy(integer=True, positive=True, prime=False)
    assert x.is_composite is None # x could be 1
    assert (x + 1).is_composite is None
    x = Dummy(positive=True, even=True, prime=False)
    assert x.is_integer is True
    assert x.is_composite is True


def test_composite(fmt, counted, composite_image, count):
    # Test that figures can be saved with and without combining multiple images
    # (on a single set of axes) into a single composite image.
    X, Y = np.meshgrid(np.arange(-5, 5, 1), np.arange(-5, 5, 1))
    Z = np.sin(Y ** 2)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 3)
    ax.imshow(Z, extent=[0, 1, 0, 1])
    ax.imshow(Z[::-1], extent=[2, 3, 0, 1])
    plt.rcParams['image.composite_image'] = composite_image
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt)
    assert buf.getvalue().count(counted) == count

