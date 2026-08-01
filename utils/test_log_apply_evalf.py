
def test_log_apply_evalf():
    value = (log(3)/log(2) - 1).evalf()
    assert value.epsilon_eq(Float("0.58496250072115618145373"))

