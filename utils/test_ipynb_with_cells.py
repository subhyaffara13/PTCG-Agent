
def test_ipynb_with_cells(mocker, log_mock):
    mi_cfg = cli.Config(**BASE_CONFIG_WITH_IPYNB_AND_CELLS.config_values)
    mi_cfg.config_values.update(MI_CONFIG.config_values)
    raw_cfg = cli.Config(**BASE_CONFIG_WITH_IPYNB_AND_CELLS.config_values)
    raw_cfg.config_values.update(RAW_CONFIG.config_values)
    cc_cfg = cli.Config(
        order=lambda block: block.name,
        no_assert=False,
        min='A',
        max='F',
        show_complexity=False,
        show_closures=False,
        average=True,
        total_average=False,
    )
    cc_cfg.config_values.update(BASE_CONFIG_WITH_IPYNB_AND_CELLS.config_values)

    mappings = {
        MIHarvester: mi_cfg,
        RawHarvester: raw_cfg,
        CCHarvester: cc_cfg,
    }
    target = 'data/'
    fnames = [
        os.path.join(DIRNAME, target),
    ]
    for h_class, cfg in mappings.items():
        for f in fnames:
            harvester = h_class([f], cfg)
            out = harvester.as_json()
            assert not any(['error' in out]), out

