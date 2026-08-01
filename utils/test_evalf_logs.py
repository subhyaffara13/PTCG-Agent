
def test_evalf_logs():
    assert NS("log(3+pi*I)", 15) == '1.46877619736226 + 0.808448792630022*I'
    assert NS("log(pi*I)", 15) == '1.14472988584940 + 1.57079632679490*I'
    assert NS('log(-1 + 0.00001)', 2) == '-1.0e-5 + 3.1*I'
    assert NS('log(100, 10, evaluate=False)', 15) == '2.00000000000000'
    assert NS('-2*I*log(-(-1)**(S(1)/9))', 15) == '-5.58505360638185'

