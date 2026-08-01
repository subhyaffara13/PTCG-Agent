
def test_log_result(mocker, stdout_mock):
    le_mock = mocker.patch('radon.cli.log_error')
    ll_mock = mocker.patch('radon.cli.log_list')
    log_mock = mocker.patch('radon.cli.log')

    h = mocker.Mock(spec=Harvester)
    h.as_json.return_value = mocker.sentinel.json
    h.as_xml.return_value = mocker.sentinel.xml
    h.as_md.return_value = mocker.sentinel.md
    h.to_terminal.side_effect = fake_to_terminal

    cli.log_result(h, json=True)
    h.as_json.assert_called_once_with()

    h.as_json.reset_mock()
    cli.log_result(h, json=True, xml=True, md=True)
    h.as_json.assert_called_once_with()
    assert h.as_xml.call_count == 0
    assert h.as_md.call_count == 0

    cli.log_result(h, xml=True)
    h.as_xml.assert_called_once_with()

    cli.log_result(h, md=True)
    h.as_md.assert_called_once_with()

    cli.log_result(h)
    h.to_terminal.assert_called_once_with()

    log_mock.assert_has_calls(
        [
            mocker.call(mocker.sentinel.json, json=True, noformat=True),
            mocker.call(
                mocker.sentinel.json, json=True, noformat=True, xml=True, md=True
            ),
            mocker.call(mocker.sentinel.xml, noformat=True, xml=True),
            mocker.call(mocker.sentinel.md, noformat=True, md=True),
            mocker.call('a', error=True),
        ]
    )
    le_mock.assert_called_once_with('mystr', indent=1)
    ll_mock.assert_has_calls(
        [mocker.call(['b']), mocker.call(('p1', 'p2'), indent=1)]
    )

