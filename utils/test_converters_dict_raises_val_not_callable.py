
def test_converters_dict_raises_val_not_callable():
    with pytest.raises(TypeError,
                match="values of the converters dictionary must be callable"):
        np.loadtxt(StringIO("1 2\n3 4"), converters={0: 1})

