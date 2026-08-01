
def test_repr_with_complex_nans(data, output, as_frame):
    # GH#53762, GH#53841
    obj = Series(np.array(data))
    if as_frame:
        obj = obj.to_frame(name="val")
        reprs = [f"{i} {val}" for i, val in enumerate(output)]
        expected = f"{'val': >{len(reprs[0])}}\n" + "\n".join(reprs)
    else:
        reprs = [f"{i}   {val}" for i, val in enumerate(output)]
        expected = "\n".join(reprs) + "\ndtype: complex128"
    assert str(obj) == expected, f"\n{obj!s}\n\n{expected}"

