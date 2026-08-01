
def test_rc_interpolation_stage():
    for val in ["data", "rgba"]:
        with mpl.rc_context({"image.interpolation_stage": val}):
            assert plt.imshow([[1, 2]]).get_interpolation_stage() == val
    for val in ["DATA", "foo", None]:
        with pytest.raises(ValueError):
            mpl.rcParams["image.interpolation_stage"] = val

