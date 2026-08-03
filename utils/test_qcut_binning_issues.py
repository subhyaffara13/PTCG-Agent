import os

def test_qcut_binning_issues(datapath):
    # see gh-1978, gh-1979
    cut_file = datapath(os.path.join("reshape", "data", "cut_data.csv"))
    arr = np.loadtxt(cut_file)
    result = qcut(arr, 20)

    starts = result.categories.left
    ends = result.categories.right
    assert (starts < ends).all()
    assert (starts[1:] <= ends[:-1]).all()

