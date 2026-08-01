
def test_to_html_round_column_headers():
    # GH 17280
    df = DataFrame([1], columns=[0.55555])
    with option_context("display.precision", 3):
        html = df.to_html(notebook=False)
        notebook = df.to_html(notebook=True)
    assert "0.55555" in html
    assert "0.556" in notebook

