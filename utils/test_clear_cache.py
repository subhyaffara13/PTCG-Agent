
def test_clear_cache(tmp_path):
    # Note: `tmp_path` is a pytest fixture, it handles cleanup
    thread_basepath = tmp_path / str(get_ident())
    thread_basepath.mkdir()

    dummy_basepath = thread_basepath / "dummy_cache_dir"
    dummy_basepath.mkdir()

    # Create three dummy dataset files for dummy dataset methods
    dummy_method_map = {}
    for i in range(4):
        dummy_method_map[f"data{i}"] = [f"data{i}.dat"]
        data_filepath = dummy_basepath / f"data{i}.dat"
        data_filepath.write_text("")

    # clear files associated to single dataset method data0
    # also test callable argument instead of list of callables
    def data0():
        pass
    _clear_cache(datasets=data0, cache_dir=dummy_basepath,
                 method_map=dummy_method_map)
    assert not os.path.exists(dummy_basepath/"data0.dat")

    # clear files associated to multiple dataset methods "data3" and "data4"
    def data1():
        pass

    def data2():
        pass
    _clear_cache(datasets=[data1, data2], cache_dir=dummy_basepath,
                 method_map=dummy_method_map)
    assert not os.path.exists(dummy_basepath/"data1.dat")
    assert not os.path.exists(dummy_basepath/"data2.dat")

    # clear multiple dataset files "data3_0.dat" and "data3_1.dat"
    # associated with dataset method "data3"
    def data4():
        pass
    # create files
    (dummy_basepath / "data4_0.dat").write_text("")
    (dummy_basepath / "data4_1.dat").write_text("")

    dummy_method_map["data4"] = ["data4_0.dat", "data4_1.dat"]
    _clear_cache(datasets=[data4], cache_dir=dummy_basepath,
                 method_map=dummy_method_map)
    assert not os.path.exists(dummy_basepath/"data4_0.dat")
    assert not os.path.exists(dummy_basepath/"data4_1.dat")

    # wrong dataset method should raise ValueError since it
    # doesn't exist in the dummy_method_map
    def data5():
        pass
    with pytest.raises(ValueError):
        _clear_cache(datasets=[data5], cache_dir=dummy_basepath,
                     method_map=dummy_method_map)

    # remove all dataset cache
    _clear_cache(datasets=None, cache_dir=dummy_basepath)
    assert not os.path.exists(dummy_basepath)

