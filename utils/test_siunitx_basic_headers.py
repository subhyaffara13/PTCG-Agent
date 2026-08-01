
def test_siunitx_basic_headers(styler):
    assert "{} & {A} & {B} & {C} \\\\" in styler.to_latex(siunitx=True)
    assert " & A & B & C \\\\" in styler.to_latex()  # default siunitx=False

