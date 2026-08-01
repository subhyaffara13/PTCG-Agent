
def test_pr4220_tripped_over_this():
    assert (
        m.Empty0().get_msg()
        == "This is really only meant to exercise successful compilation."
    )

