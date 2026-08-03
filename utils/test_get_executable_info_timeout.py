import subprocess

def test_get_executable_info_timeout(mock_check_output):
    """
    Test that _get_executable_info raises ExecutableNotFoundError if the
    command times out.
    """

    mock_check_output.side_effect = subprocess.TimeoutExpired(cmd=['mock'], timeout=30)

    with pytest.raises(matplotlib.ExecutableNotFoundError, match='Timed out'):
        matplotlib._get_executable_info.__wrapped__('inkscape')

