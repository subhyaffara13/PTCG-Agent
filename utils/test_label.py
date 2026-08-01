
def test_label(styler, env):
    assert "\n\\label{text}" in styler.to_latex(label="text", environment=env)
    styler.set_table_styles([{"selector": "label", "props": ":{more §text}"}])
    assert "\n\\label{more :text}" in styler.to_latex(environment=env)


def test_label():
    s = Sankey(flows=[0.25], labels=['First'], orientations=[-1])
    assert s.diagrams[0].texts[0].get_text() == 'First\n0.25'

