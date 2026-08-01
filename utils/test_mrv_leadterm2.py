
def test_mrv_leadterm2():
    #Gruntz: p51, 3.25
    assert mrv_leadterm((log(exp(x) + x) - x)/log(exp(x) + log(x))*exp(x), x) == \
        (1, 0)

