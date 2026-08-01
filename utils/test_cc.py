
def test_cc(mocker, log_mock):
    harv_mock = mocker.patch('radon.cli.CCHarvester')
    harv_mock.return_value = mocker.sentinel.harvester

    cli.cc(['-'], json=True)

    harv_mock.assert_called_once_with(
        ['-'],
        cli.Config(
            min='A',
            max='F',
            exclude=None,
            ignore=None,
            show_complexity=False,
            average=False,
            order=getattr(cc_mod, 'SCORE'),
            no_assert=False,
            total_average=False,
            show_closures=False,
            include_ipynb=False,
            ipynb_cells=False,
        ),
    )
    log_mock.assert_called_once_with(
        mocker.sentinel.harvester,
        codeclimate=False,
        json=True,
        stream=sys.stdout,
        xml=False,
        md=False
    )

