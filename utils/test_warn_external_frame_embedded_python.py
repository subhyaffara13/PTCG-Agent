
def test_warn_external_frame_embedded_python():
    with patch.object(cbook, "sys") as mock_sys:
        mock_sys._getframe = Mock(return_value=None)
        with pytest.warns(UserWarning, match=r"\Adummy\Z"):
            _api.warn_external("dummy")

