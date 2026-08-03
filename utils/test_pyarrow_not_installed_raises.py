import re

def test_pyarrow_not_installed_raises():
    msg = re.escape("pyarrow>=13.0.0 is required for PyArrow backed")

    with pytest.raises(ImportError, match=msg):
        StringDtype(storage="pyarrow")

    with pytest.raises(ImportError, match=msg):
        ArrowStringArray([])

    with pytest.raises(ImportError, match=msg):
        ArrowStringArray._from_sequence(["a", None, "b"])

