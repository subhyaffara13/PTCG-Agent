
def test_print_IndexedBase():
    assert mathml(IndexedBase(a)[b], printer='presentation') == \
        '<msub><mi>a</mi><mi>b</mi></msub>'
    assert mathml(IndexedBase(a)[b, c, d], printer='presentation') == \
        '<msub><mi>a</mi><mrow><mo>(</mo><mi>b</mi><mo>,</mo><mi>c</mi><mo>,</mo><mi>d</mi><mo>)</mo></mrow></msub>'
    assert mathml(IndexedBase(a)[b]*IndexedBase(c)[d]*IndexedBase(e),
                  printer='presentation') == \
                  '<mrow><msub><mi>a</mi><mi>b</mi></msub><mo>&InvisibleTimes;'\
                  '</mo><msub><mi>c</mi><mi>d</mi></msub><mo>&InvisibleTimes;</mo><mi>e</mi></mrow>'

