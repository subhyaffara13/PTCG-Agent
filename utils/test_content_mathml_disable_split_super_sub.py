
def test_content_mathml_disable_split_super_sub():
    mp = MathMLContentPrinter()
    assert mp.doprint(Symbol('u_b')) == '<ci><mml:msub><mml:mi>u</mml:mi><mml:mi>b</mml:mi></mml:msub></ci>'
    mp = MathMLContentPrinter({'disable_split_super_sub': False})
    assert mp.doprint(Symbol('u_b')) == '<ci><mml:msub><mml:mi>u</mml:mi><mml:mi>b</mml:mi></mml:msub></ci>'
    mp = MathMLContentPrinter({'disable_split_super_sub': True})
    assert mp.doprint(Symbol('u_b')) == '<ci>u_b</ci>'

