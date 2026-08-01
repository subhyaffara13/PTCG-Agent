
def test_gh_19659(tmp_path):
    d = {
        "char_array": np.array([list("char"), list("char")], dtype="U1"),
        "string_array": np.array(["string", "string"]),
        }
    outfile = tmp_path / "tmp.mat"
    # should not error:
    savemat(outfile, d, format="4")

