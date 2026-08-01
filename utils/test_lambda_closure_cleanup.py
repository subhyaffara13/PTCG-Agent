
def test_lambda_closure_cleanup():
    m.test_lambda_closure_cleanup()
    cstats = m.payload_cstats()
    assert cstats.alive() == 0
    assert cstats.copy_constructions == 1
    assert cstats.move_constructions >= 1

