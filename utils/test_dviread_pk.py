
def test_dviread_pk(tmp_path):
    (tmp_path / "test.tex").write_text(r"""
        \documentclass{article}
        \usepackage{concmath}
        \pagestyle{empty}
        \begin{document}
        Hi!
        \end{document}
        """)
    subprocess_run_for_testing(
        ["latex", "-no-shell-escape", "test.tex"],
        cwd=tmp_path, check=True, capture_output=True)
    with dr.Dvi(tmp_path / "test.dvi", None) as dvi:
        pages = [*dvi]
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
    correct = [{
        'boxes': [],
        'text': [
            [5046272, 4128768, 'H?', 'ccr10.600pk', 9.96, {}],
            [5530510, 4128768, 'i?', 'ccr10.600pk', 9.96, {}],
            [5716195, 4128768, '!?', 'ccr10.600pk', 9.96, {}],
        ],
    }]
    assert data == correct

