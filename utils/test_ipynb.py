import os
from pathlib import Path


def test_ipynb(log_mock):
    mi_cfg = cli.Config(**BASE_CONFIG_WITH_IPYNB.config_values)
    mi_cfg.config_values.update(MI_CONFIG.config_values)
    raw_cfg = cli.Config(**BASE_CONFIG_WITH_IPYNB.config_values)
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
    cc_cfg.config_values.update(BASE_CONFIG_WITH_IPYNB.config_values)

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


def test_ipynb():
    nb_path = Path(__file__).parent / 'data/test_inline_01.ipynb'

    with TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir, "out.ipynb")

        subprocess_run_for_testing(
            ["jupyter", "nbconvert", "--to", "notebook",
             "--execute", "--ExecutePreprocessor.timeout=500",
             "--output", str(out_path), str(nb_path)],
            env={**os.environ, "IPYTHONDIR": tmpdir},
            check=True)
        with out_path.open() as out:
            nb = nbformat.read(out, nbformat.current_nbformat)

    errors = [output for cell in nb.cells for output in cell.get("outputs", [])
              if output.output_type == "error"]
    assert not errors

    import IPython
    if IPython.version_info[:2] >= (8, 24):
        expected_backend = "inline"
    else:
        # This code can be removed when Python 3.12, the latest version supported by
        # IPython < 8.24, reaches end-of-life in late 2028.
        expected_backend = "module://matplotlib_inline.backend_inline"
    backend_outputs = nb.cells[2]["outputs"]
    assert backend_outputs[0]["data"]["text/plain"] == f"'{expected_backend}'"

    image = nb.cells[1]["outputs"][1]["data"]
    assert image["text/plain"] == "<Figure size 300x200 with 1 Axes>"
    assert "image/png" in image


def test_ipynb():
    nb_path = Path(__file__).parent / 'data/test_nbagg_01.ipynb'

    with TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir, "out.ipynb")
        subprocess_run_for_testing(
            ["jupyter", "nbconvert", "--to", "notebook",
             "--execute", "--ExecutePreprocessor.timeout=500",
             "--output", str(out_path), str(nb_path)],
            env={**os.environ, "IPYTHONDIR": tmpdir},
            check=True)
        with out_path.open() as out:
            nb = nbformat.read(out, nbformat.current_nbformat)

    errors = [output for cell in nb.cells for output in cell.get("outputs", [])
              if output.output_type == "error"]
    assert not errors

    import IPython
    if IPython.version_info[:2] >= (8, 24):
        expected_backend = "notebook"
    else:
        # This code can be removed when Python 3.12, the latest version supported by
        # IPython < 8.24, reaches end-of-life in late 2028.
        expected_backend = "nbAgg"
    backend_outputs = nb.cells[2]["outputs"]
    assert backend_outputs[0]["data"]["text/plain"] == f"'{expected_backend}'"

