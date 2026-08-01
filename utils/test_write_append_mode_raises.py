
def test_write_append_mode_raises(tmp_excel):
    msg = "Append mode is not supported with odf!"

    with pytest.raises(ValueError, match=msg):
        ExcelWriter(tmp_excel, engine="odf", mode="a")


def test_write_append_mode_raises(tmp_excel):
    msg = "Append mode is not supported with xlsxwriter!"

    with pytest.raises(ValueError, match=msg):
        ExcelWriter(tmp_excel, engine="xlsxwriter", mode="a")

