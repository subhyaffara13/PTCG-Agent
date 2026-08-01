
def test_apply_map_header(method, axis):
    # GH 41893
    df = DataFrame({"A": [0, 0], "B": [1, 1]}, index=["C", "D"])
    func = {
        "apply": lambda s: ["attr: val" if ("A" in v or "C" in v) else "" for v in s],
        "map": lambda v: "attr: val" if ("A" in v or "C" in v) else "",
    }

    # test execution added to todo
    result = getattr(df.style, f"{method}_index")(func[method], axis=axis)
    assert len(result._todo) == 1
    assert len(getattr(result, f"ctx_{axis}")) == 0

    # test ctx object on compute
    result._compute()
    expected = {
        (0, 0): [("attr", "val")],
    }
    assert getattr(result, f"ctx_{axis}") == expected

