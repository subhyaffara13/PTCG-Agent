
def test_cc_as_json_xml(cc_config, mocker):
    d2x_mock = mocker.patch('radon.cli.harvest.dict_to_xml')
    to_dicts_mock = mocker.MagicMock()
    to_dicts_mock.return_value = {'a': {'rank': 'A'}}

    h = harvest.CCHarvester([], cc_config)
    h._to_dicts = to_dicts_mock
    assert h.as_json() == '{"a": {"rank": "A"}}'

    h.as_xml()
    assert d2x_mock.called
    d2x_mock.assert_called_with(to_dicts_mock.return_value)
    assert to_dicts_mock.call_count == 2

