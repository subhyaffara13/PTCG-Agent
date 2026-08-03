import re

def test_check_package_data(package_data, expected_message):
    if expected_message is None:
        assert check_package_data(None, 'package_data', package_data) is None
    else:
        with pytest.raises(DistutilsSetupError, match=re.escape(expected_message)):
            check_package_data(None, 'package_data', package_data)

