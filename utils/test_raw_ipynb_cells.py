import json
import os

def test_raw_ipynb_cells(log_mock):
    raw_cfg = cli.Config(**BASE_CONFIG_WITH_IPYNB_AND_CELLS.config_values)

    target = os.path.join(DIRNAME, 'data/example.ipynb')
    harvester = RawHarvester([DIRNAME], raw_cfg)
    out = json.loads(harvester.as_json())
    cell_target = target + ":[3]"
    assert target in out
    assert cell_target in out
    assert out[cell_target]['loc'] == 52
    assert out[cell_target]['lloc'] == 27
    assert out[cell_target]['sloc'] == 27
    assert out[cell_target]['comments'] == 3
    assert out[cell_target]['multi'] == 10
    assert out[cell_target]['blank'] == 13
    assert out[cell_target]['single_comments'] == 2

