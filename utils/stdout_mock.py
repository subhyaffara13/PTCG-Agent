
def stdout_mock(mocker):
    return mocker.patch('radon.cli.sys.stdout.write')

