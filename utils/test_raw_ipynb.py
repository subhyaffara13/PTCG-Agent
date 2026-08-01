
def test_raw_ipynb(log_mock):
    raw_cfg = cli.Config(**BASE_CONFIG_WITH_IPYNB.config_values)

    target = os.path.join(DIRNAME, 'data/example.ipynb')
    harvester = RawHarvester([DIRNAME], raw_cfg)
    out = json.loads(harvester.as_json())
    assert harvester.config.include_ipynb == True
    assert target in out
    assert out[target]['loc'] == 63
    assert out[target]['lloc'] == 37
    assert out[target]['sloc'] == 37
    assert out[target]['comments'] == 3
    assert out[target]['multi'] == 10
    assert out[target]['blank'] == 14
    assert out[target]['single_comments'] == 2

