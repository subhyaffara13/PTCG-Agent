
def test_many_strl(temp_file, version):
    n = 65534
    df = DataFrame(np.arange(n), columns=["col"])
    lbls = ["".join(v) for v in itertools.product(*([string.ascii_letters] * 3))]
    value_labels = {"col": {i: lbls[i] for i in range(n)}}
    df.to_stata(temp_file, value_labels=value_labels, version=version)

