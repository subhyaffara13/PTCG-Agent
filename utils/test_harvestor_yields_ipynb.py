import os

def test_harvestor_yields_ipynb(log_mock):
    '''Test that Harvester will try ipynb files when configured'''
    target = os.path.join(DIRNAME, 'data/example.ipynb')
    harvester = Harvester([DIRNAME], BASE_CONFIG_WITH_IPYNB)
    filenames = list(harvester._iter_filenames())
    assert _is_python_file(target)
    assert len(filenames) == 1
    assert target in filenames

