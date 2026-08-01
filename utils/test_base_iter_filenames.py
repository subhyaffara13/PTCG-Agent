
def test_base_iter_filenames(base_config, mocker):
    iter_mock = mocker.patch('radon.cli.harvest.iter_filenames')
    h = harvest.Harvester([], base_config)
    h._iter_filenames()

    iter_mock.assert_called_with([], base_config.exclude, base_config.ignore)

