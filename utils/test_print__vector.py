
def test_print_Vector():
    ACS = CoordSys3D('A')
    assert mathml(Cross(ACS.i, ACS.j*ACS.x*3 + ACS.k), printer='presentation') == \
        '<mrow><msub><mover><mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xD7;</mo><mrow><mo>(</mo><mrow>'\
        '<mrow><mo>(</mo><mrow><mn>3</mn><mo>&InvisibleTimes;</mo><msub>'\
        '<mi mathvariant="bold">x</mi><mi mathvariant="bold">A</mi></msub>'\
        '</mrow><mo>)</mo></mrow><mo>&InvisibleTimes;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>+</mo><msub><mover>'\
        '<mi mathvariant="bold">k</mi><mo>^</mo></mover><mi mathvariant="bold">'\
        'A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Cross(ACS.i, ACS.j), printer='presentation') == \
        '<mrow><msub><mover><mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xD7;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow>'
    assert mathml(x*Cross(ACS.i, ACS.j), printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mrow><mo>(</mo><mrow><msub><mover>'\
        '<mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xD7;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Cross(x*ACS.i, ACS.j), printer='presentation') == \
        '<mrow><mo>-</mo><mrow><msub><mover><mi mathvariant="bold">j</mi>'\
        '<mo>^</mo></mover><mi mathvariant="bold">A</mi></msub>'\
        '<mo>&#xD7;</mo><mrow><mo>(</mo><mrow><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow>'\
        '<mo>&InvisibleTimes;</mo><msub><mover><mi mathvariant="bold">i</mi>'\
        '<mo>^</mo></mover><mi mathvariant="bold">A</mi></msub></mrow>'\
        '<mo>)</mo></mrow></mrow></mrow>'
    assert mathml(Curl(3*ACS.x*ACS.j), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mo>&#xD7;</mo><mrow><mo>(</mo><mrow><mrow><mo>(</mo>'\
        '<mrow><mn>3</mn><mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">x</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow><mo>&InvisibleTimes;</mo>'\
        '<msub><mover><mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Curl(3*x*ACS.x*ACS.j), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mo>&#xD7;</mo><mrow><mo>(</mo><mrow><mrow><mo>(</mo><mrow>'\
        '<mn>3</mn><mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">x'\
        '</mi><mi mathvariant="bold">A</mi></msub><mo>&InvisibleTimes;</mo>'\
        '<mi>x</mi></mrow><mo>)</mo></mrow><mo>&InvisibleTimes;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(x*Curl(3*ACS.x*ACS.j), printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mrow><mo>(</mo><mrow><mo>&#x2207;</mo>'\
        '<mo>&#xD7;</mo><mrow><mo>(</mo><mrow><mrow><mo>(</mo><mrow><mn>3</mn>'\
        '<mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">x</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow>'\
        '<mo>&InvisibleTimes;</mo><msub><mover><mi mathvariant="bold">j</mi>'\
        '<mo>^</mo></mover><mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo>'\
        '</mrow></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Curl(3*x*ACS.x*ACS.j + ACS.i), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mo>&#xD7;</mo><mrow><mo>(</mo><mrow><msub><mover>'\
        '<mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>+</mo><mrow><mo>(</mo><mrow>'\
        '<mn>3</mn><mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">x'\
        '</mi><mi mathvariant="bold">A</mi></msub><mo>&InvisibleTimes;</mo>'\
        '<mi>x</mi></mrow><mo>)</mo></mrow><mo>&InvisibleTimes;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Divergence(3*ACS.x*ACS.j), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mo>&#xB7;</mo><mrow><mo>(</mo><mrow><mrow><mo>(</mo>'\
        '<mrow><mn>3</mn><mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">x'\
        '</mi><mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow>'\
        '<mo>&InvisibleTimes;</mo><msub><mover><mi mathvariant="bold">j</mi>'\
        '<mo>^</mo></mover><mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(x*Divergence(3*ACS.x*ACS.j), printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mrow><mo>(</mo><mrow><mo>&#x2207;</mo>'\
        '<mo>&#xB7;</mo><mrow><mo>(</mo><mrow><mrow><mo>(</mo><mrow><mn>3</mn>'\
        '<mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">x</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow>'\
        '<mo>&InvisibleTimes;</mo><msub><mover><mi mathvariant="bold">j</mi>'\
        '<mo>^</mo></mover><mi mathvariant="bold">A</mi></msub></mrow>'\
        '<mo>)</mo></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Divergence(3*x*ACS.x*ACS.j + ACS.i), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mo>&#xB7;</mo><mrow><mo>(</mo><mrow><msub><mover>'\
        '<mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>+</mo><mrow><mo>(</mo><mrow>'\
        '<mn>3</mn><mo>&InvisibleTimes;</mo><msub>'\
        '<mi mathvariant="bold">x</mi><mi mathvariant="bold">A</mi></msub>'\
        '<mo>&InvisibleTimes;</mo><mi>x</mi></mrow><mo>)</mo></mrow>'\
        '<mo>&InvisibleTimes;</mo><msub><mover><mi mathvariant="bold">j</mi>'\
        '<mo>^</mo></mover><mi mathvariant="bold">A</mi></msub></mrow>'\
        '<mo>)</mo></mrow></mrow>'
    assert mathml(Dot(ACS.i, ACS.j*ACS.x*3+ACS.k), printer='presentation') == \
        '<mrow><msub><mover><mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xB7;</mo><mrow><mo>(</mo><mrow>'\
        '<mrow><mo>(</mo><mrow><mn>3</mn><mo>&InvisibleTimes;</mo><msub>'\
        '<mi mathvariant="bold">x</mi><mi mathvariant="bold">A</mi></msub>'\
        '</mrow><mo>)</mo></mrow><mo>&InvisibleTimes;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>+</mo><msub><mover>'\
        '<mi mathvariant="bold">k</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Dot(ACS.i, ACS.j), printer='presentation') == \
        '<mrow><msub><mover><mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xB7;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow>'
    assert mathml(Dot(x*ACS.i, ACS.j), printer='presentation') == \
        '<mrow><msub><mover><mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xB7;</mo><mrow><mo>(</mo><mrow>'\
        '<mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>&InvisibleTimes;</mo><msub><mover>'\
        '<mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(x*Dot(ACS.i, ACS.j), printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mrow><mo>(</mo><mrow><msub><mover>'\
        '<mi mathvariant="bold">i</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xB7;</mo><msub><mover>'\
        '<mi mathvariant="bold">j</mi><mo>^</mo></mover>'\
        '<mi mathvariant="bold">A</mi></msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Gradient(ACS.x), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><msub><mi mathvariant="bold">x</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow>'
    assert mathml(Gradient(ACS.x + 3*ACS.y), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mrow><mo>(</mo><mrow><msub><mi mathvariant="bold">'\
        'x</mi><mi mathvariant="bold">A</mi></msub><mo>+</mo><mrow><mn>3</mn>'\
        '<mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">y</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(x*Gradient(ACS.x), printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mrow><mo>(</mo><mrow><mo>&#x2207;</mo>'\
        '<msub><mi mathvariant="bold">x</mi><mi mathvariant="bold">A</mi>'\
        '</msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Gradient(x*ACS.x), printer='presentation') == \
        '<mrow><mo>&#x2207;</mo><mrow><mo>(</mo><mrow><msub><mi mathvariant="bold">'\
        'x</mi><mi mathvariant="bold">A</mi></msub><mo>&InvisibleTimes;</mo>'\
        '<mi>x</mi></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Cross(ACS.z, ACS.x), printer='presentation') == \
        '<mrow><mo>-</mo><mrow><msub><mi mathvariant="bold">x</mi>'\
        '<mi mathvariant="bold">A</mi></msub><mo>&#xD7;</mo><msub>'\
        '<mi mathvariant="bold">z</mi><mi mathvariant="bold">A</mi></msub></mrow></mrow>'
    assert mathml(Laplacian(ACS.x), printer='presentation') == \
        '<mrow><mo>&#x2206;</mo><msub><mi mathvariant="bold">x</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow>'
    assert mathml(Laplacian(ACS.x + 3*ACS.y), printer='presentation') == \
        '<mrow><mo>&#x2206;</mo><mrow><mo>(</mo><mrow><msub><mi mathvariant="bold">'\
        'x</mi><mi mathvariant="bold">A</mi></msub><mo>+</mo><mrow><mn>3</mn>'\
        '<mo>&InvisibleTimes;</mo><msub><mi mathvariant="bold">y</mi>'\
        '<mi mathvariant="bold">A</mi></msub></mrow></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(x*Laplacian(ACS.x), printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mrow><mo>(</mo><mrow><mo>&#x2206;</mo>'\
        '<msub><mi mathvariant="bold">x</mi><mi mathvariant="bold">A</mi>'\
        '</msub></mrow><mo>)</mo></mrow></mrow>'
    assert mathml(Laplacian(x*ACS.x), printer='presentation') == \
        '<mrow><mo>&#x2206;</mo><mrow><mo>(</mo><mrow><msub><mi mathvariant="bold">'\
        'x</mi><mi mathvariant="bold">A</mi></msub><mo>&InvisibleTimes;</mo>'\
        '<mi>x</mi></mrow><mo>)</mo></mrow></mrow>'

