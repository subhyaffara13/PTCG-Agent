
def test_cc_gobble(cc_config, mocker):
    sr_mock = mocker.patch('radon.cli.harvest.sorted_results')
    cc_mock = mocker.patch('radon.cli.harvest.cc_visit')
    cc_mock.return_value = []
    fobj = mocker.MagicMock()
    fobj.read.return_value = mocker.sentinel.one

    h = harvest.CCHarvester([], cc_config)
    h.config.show_closures = True
    h.gobble(fobj)

    assert fobj.read.called
    cc_mock.assert_called_with(
        mocker.sentinel.one, no_assert=cc_config.no_assert
    )
    sr_mock.assert_called_with([], order=cc_config.order)

