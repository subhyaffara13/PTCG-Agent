
def test_apply_map_header_mi(mi_styler, method, axis):
    # GH 41893
    func = {
        "apply": lambda s: ["attr: val;" if "b" in v else "" for v in s],
        "map": lambda v: "attr: val" if "b" in v else "",
    }
    result = getattr(mi_styler, f"{method}_index")(func[method], axis=axis)._compute()
    expected = {(1, 1): [("attr", "val")]}
    assert getattr(result, f"ctx_{axis}") == expected

