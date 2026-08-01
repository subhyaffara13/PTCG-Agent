
def test_mi_gobble(mi_config, mocker):
    mv_mock = mocker.patch('radon.cli.harvest.mi_visit')
    fobj = mocker.MagicMock()
    fobj.read.return_value = mocker.sentinel.one
    mv_mock.return_value = 23.5

    h = harvest.MIHarvester([], mi_config)
    result = h.gobble(fobj)

    assert fobj.read.call_count == 1
    mv_mock.assert_called_once_with(mocker.sentinel.one, mi_config.multi)
    assert result == {'mi': 23.5, 'rank': 'A'}

