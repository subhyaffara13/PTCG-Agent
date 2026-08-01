
def test_use_small_element():
    # Test whether we're using small data element or not
    sio = BytesIO()
    wtr = MatFile5Writer(sio)
    # First check size for no sde for name
    arr = np.zeros(10)
    wtr.put_variables({'aaaaa': arr})
    w_sz = len(sio.getvalue())
    # Check small name results in largish difference in size
    sio.truncate(0)
    sio.seek(0)
    wtr.put_variables({'aaaa': arr})
    assert_(w_sz - len(sio.getvalue()) > 4)
    # Whereas increasing name size makes less difference
    sio.truncate(0)
    sio.seek(0)
    wtr.put_variables({'aaaaaa': arr})
    assert_(len(sio.getvalue()) - w_sz < 4)

