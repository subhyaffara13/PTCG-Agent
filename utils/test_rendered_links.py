
def test_rendered_links(type, text, exp, found):
    if type == "data":
        df = DataFrame([text])
        styler = df.style.format(hyperlinks="html")
    else:
        df = DataFrame([0], index=[text])
        styler = df.style.format_index(hyperlinks="html")

    rendered = f'<a href="{found}" target="_blank">{found}</a>'
    result = styler.to_html()
    assert (rendered in result) is exp
    assert (text in result) is not exp  # test conversion done when expected and not


def test_rendered_links():
    # note the majority of testing is done in test_html.py: test_rendered_links
    # these test only the alternative latex format is functional
    df = DataFrame(["text www.domain.com text"])
    result = df.style.format(hyperlinks="latex").to_latex()
    assert r"text \href{www.domain.com}{www.domain.com} text" in result

