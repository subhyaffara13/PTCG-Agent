import re

def test_text_re_im():
    assert latex(im(x), gothic_re_im=True) == r'\Im{\left(x\right)}'
    assert latex(im(x), gothic_re_im=False) == r'\operatorname{im}{\left(x\right)}'
    assert latex(re(x), gothic_re_im=True) == r'\Re{\left(x\right)}'
    assert latex(re(x), gothic_re_im=False) == r'\operatorname{re}{\left(x\right)}'

