
def test_config_converts_types(mocker):
    test_config = ConfigParser()
    test_config.read_string(
        u'''
        [radon]
        str_test = B
        int_test = 19
        bool_test = true
        '''
    )
    config_mock = mocker.patch('radon.cli.FileConfig.file_config')
    config_mock.return_value = test_config

    cfg = cli.FileConfig()
    assert cfg.get_value('bool_test', bool, False) == True
    assert cfg.get_value('str_test', str, 'x') == 'B'
    assert cfg.get_value('missing_test', str, 'Y') == 'Y'
    assert cfg.get_value('int_test', int, 10) == 19

