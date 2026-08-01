
def test_log_error(mocker, stdout_mock):
    reset_mock = mocker.patch('radon.cli.RESET')
    red_mock = mocker.patch('radon.cli.RED')
    bright_mock = mocker.patch('radon.cli.BRIGHT')

    bright_mock.__str__.return_value = '@'
    red_mock.__str__.return_value = '<|||>'
    reset_mock.__str__.return_value = '__R__'

    cli.log_error('mystr')

    stdout_mock.assert_called_once_with('@<|||>ERROR__R__: mystr\n')

