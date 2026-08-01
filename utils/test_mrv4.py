
def test_mrv4():
    ln = log
    assert mmrv((ln(ln(x) + ln(ln(x))) - ln(ln(x)))/ln(ln(x) + ln(ln(ln(x))))*ln(x),
            x) == {x}
    assert mmrv(log(log(x*exp(x*exp(x)) + 1)) - exp(exp(log(log(x) + 1/x))), x) == \
        {exp(x*exp(x))}

