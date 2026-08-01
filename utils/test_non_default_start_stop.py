
def test_non_default_start_stop(function, start, stop, expected):
    a = np.array([["--🐍--", "--🦜--"],
                  ["-🐍---", "-🦜---"]], "T")
    indx = function(a, "🐍", start, stop)
    assert_array_equal(indx, expected)

