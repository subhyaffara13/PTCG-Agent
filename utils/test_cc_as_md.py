
def test_cc_as_md(cc_config, mocker):
    d2md_mock = mocker.patch('radon.cli.harvest.dict_to_md')
    to_dicts_mock = mocker.MagicMock()
    to_dicts_mock.return_value = {'a': {'rank': 'A'}}

    h = harvest.CCHarvester([], cc_config)
    h._to_dicts = to_dicts_mock
    assert h.as_md()
    assert d2md_mock.called
    d2md_mock.assert_called_with(to_dicts_mock.return_value)
    assert to_dicts_mock.call_count == 1

