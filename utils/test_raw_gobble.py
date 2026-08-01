
def test_raw_gobble(raw_config, mocker):
    r2d_mock = mocker.patch('radon.cli.harvest.raw_to_dict')
    analyze_mock = mocker.patch('radon.cli.harvest.analyze')
    fobj = mocker.MagicMock()
    fobj.read.return_value = mocker.sentinel.one
    analyze_mock.return_value = mocker.sentinel.two

    h = harvest.RawHarvester([], raw_config)
    h.gobble(fobj)

    assert fobj.read.call_count == 1
    analyze_mock.assert_called_once_with(mocker.sentinel.one)
    r2d_mock.assert_called_once_with(mocker.sentinel.two)

