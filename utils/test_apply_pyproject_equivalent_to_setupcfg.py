
def test_apply_pyproject_equivalent_to_setupcfg(url, monkeypatch, tmp_path):
    monkeypatch.setattr(expand, "read_attr", Mock(return_value="0.0.1"))
    monkeypatch.setattr(
        Distribution, "_expand_patterns", Mock(side_effect=_mock_expand_patterns)
    )
    setupcfg_example = retrieve_file(url)
    pyproject_example = Path(tmp_path, "pyproject.toml")
    setupcfg_text = setupcfg_example.read_text(encoding="utf-8")
    toml_config = LiteTranslator().translate(setupcfg_text, "setup.cfg")
    pyproject_example.write_text(toml_config, encoding="utf-8")

    dist_toml = pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject_example)
    dist_cfg = setupcfg.apply_configuration(makedist(tmp_path), setupcfg_example)

    pkg_info_toml = core_metadata(dist_toml)
    pkg_info_cfg = core_metadata(dist_cfg)
    assert pkg_info_toml == pkg_info_cfg

    if any(getattr(d, "license_files", None) for d in (dist_toml, dist_cfg)):
        assert set(dist_toml.license_files) == set(dist_cfg.license_files)

    if any(getattr(d, "entry_points", None) for d in (dist_toml, dist_cfg)):
        print(dist_cfg.entry_points)
        ep_toml = {
            (k, *sorted(i.replace(" ", "") for i in v))
            for k, v in dist_toml.entry_points.items()
        }
        ep_cfg = {
            (k, *sorted(i.replace(" ", "") for i in v))
            for k, v in dist_cfg.entry_points.items()
        }
        assert ep_toml == ep_cfg

    if any(getattr(d, "package_data", None) for d in (dist_toml, dist_cfg)):
        pkg_data_toml = {(k, *sorted(v)) for k, v in dist_toml.package_data.items()}
        pkg_data_cfg = {(k, *sorted(v)) for k, v in dist_cfg.package_data.items()}
        assert pkg_data_toml == pkg_data_cfg

    if any(getattr(d, "data_files", None) for d in (dist_toml, dist_cfg)):
        data_files_toml = {(k, *sorted(v)) for k, v in dist_toml.data_files}
        data_files_cfg = {(k, *sorted(v)) for k, v in dist_cfg.data_files}
        assert data_files_toml == data_files_cfg

    assert set(dist_toml.install_requires) == set(dist_cfg.install_requires)
    if any(getattr(d, "extras_require", None) for d in (dist_toml, dist_cfg)):
        extra_req_toml = {(k, *sorted(v)) for k, v in dist_toml.extras_require.items()}
        extra_req_cfg = {(k, *sorted(v)) for k, v in dist_cfg.extras_require.items()}
        assert extra_req_toml == extra_req_cfg

