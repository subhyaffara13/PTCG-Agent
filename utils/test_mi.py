
def test_mi(mocker, log_mock):
    harv_mock = mocker.patch('radon.cli.MIHarvester')
    harv_mock.return_value = mocker.sentinel.harvester

    cli.mi(['-'], show=True, multi=False)

    harv_mock.assert_called_once_with(
        ['-'],
        cli.Config(
            min='A',
            max='C',
            exclude=None,
            ignore=None,
            show=True,
            multi=False,
            sort=False,
            include_ipynb=False,
            ipynb_cells=False,
        ),
    )
    log_mock.assert_called_once_with(
        mocker.sentinel.harvester, stream=sys.stdout, json=False
    )

