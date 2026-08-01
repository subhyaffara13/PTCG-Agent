
def test_log_list(stdout_mock):
    cli.log_list([])
    cli.log_list(['msg'])

    stdout_mock.assert_called_once_with('msg\n')

