import sys

def test_raw(mocker, log_mock):
    harv_mock = mocker.patch('radon.cli.RawHarvester')
    harv_mock.return_value = mocker.sentinel.harvester

    cli.raw(['-'], summary=True, json=True)

    harv_mock.assert_called_once_with(
        ['-'],
        cli.Config(
            exclude=None,
            ignore=None,
            summary=True,
            include_ipynb=False,
            ipynb_cells=False,
        ),
    )
    log_mock.assert_called_once_with(
        mocker.sentinel.harvester, stream=sys.stdout, json=True
    )

