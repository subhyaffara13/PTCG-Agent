
def test_dviread(tmp_path, engine, monkeypatch):
    dirpath = Path(__file__).parent / "baseline_images/dviread"
    shutil.copy(dirpath / "test.tex", tmp_path)
    shutil.copy(cbook._get_data_path("fonts/ttf/DejaVuSans.ttf"), tmp_path)
    cmd, fmt = {
        "pdflatex": (["latex", "-no-shell-escape"], "dvi"),
        "xelatex": (["xelatex", "-no-pdf", "-no-shell-escape"], "xdv"),
        "lualatex": (["lualatex", "-output-format=dvi", "-no-shell-escape"], "dvi"),
    }[engine]
    if shutil.which(cmd[0]) is None:
        pytest.skip(f"{cmd[0]} is not available")
    subprocess_run_for_testing(
        [*cmd, "test.tex"], cwd=tmp_path, check=True, capture_output=True)
    # dviread must be run from the tmppath directory because {xe,lua}tex output
    # records the path to DejaVuSans.ttf as it is written in the tex source,
    # i.e. as a relative path.
    monkeypatch.chdir(tmp_path)
    with dr.Dvi(tmp_path / f"test.{fmt}", None) as dvi:
        try:
            pages = [*dvi]
        except FileNotFoundError as exc:
            for note in getattr(exc, "__notes__", []):
                if "too-old version of luaotfload" in note:
                    pytest.skip(note)
            raise
    data = [
        {
            "text": [
                [
                    t.x, t.y,
                    t._as_unicode_or_name(),
                    t.font.resolve_path().name,
                    round(t.font.size, 2),
                    t.font.effects,
                ] for t in page.text
            ],
            "boxes": [[b.x, b.y, b.height, b.width] for b in page.boxes]
        } for page in pages
    ]
    correct = json.loads((dirpath / f"{engine}.json").read_text())
    assert data == correct

