
def test_licenses_preserve_folder_structure(licenses_dist, monkeypatch, tmp_path):
    monkeypatch.chdir(licenses_dist)
    bdist_wheel_cmd(bdist_dir=str(tmp_path)).run()
    print(os.listdir("dist"))
    with ZipFile("dist/licenses_dist-1.0-py3-none-any.whl") as wf:
        default_files = {name.replace("dummy_", "licenses_") for name in DEFAULT_FILES}
        license_files = {
            "licenses_dist-1.0.dist-info/licenses/LICENSE",
            "licenses_dist-1.0.dist-info/licenses/src/vendor/LICENSE",
        }
        assert set(wf.namelist()) == default_files | license_files
        metadata = wf.read("licenses_dist-1.0.dist-info/METADATA").decode("utf8")
        assert "License-File: src/vendor/LICENSE" in metadata
        assert "License-File: LICENSE" in metadata

