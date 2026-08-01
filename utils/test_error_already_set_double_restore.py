
def test_error_already_set_double_restore():
    m.test_error_already_set_double_restore(True)  # dry_run
    with pytest.raises(RuntimeError) as excinfo:
        m.test_error_already_set_double_restore(False)
    assert str(excinfo.value) == (
        "Internal error: pybind11::detail::error_fetch_and_normalize::restore()"
        " called a second time. ORIGINAL ERROR: ValueError: Random error."
    )

