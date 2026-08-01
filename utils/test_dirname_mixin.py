
def test_dirname_mixin() -> None:
    # GH37173

    class X(accessor.DirNamesMixin):
        x = 1
        y: int

        def __init__(self) -> None:
            self.z = 3

    result = [attr_name for attr_name in dir(X()) if not attr_name.startswith("_")]

    assert result == ["x", "z"]

