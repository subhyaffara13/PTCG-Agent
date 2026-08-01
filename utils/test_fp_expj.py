
def test_fp_expj():
    assert ae(fp.expj(0), (1.0 + 0.0j))
    assert ae(fp.expj(1), (0.5403023058681397174 + 0.84147098480789650665j))
    assert ae(fp.expj(2), (-0.416146836547142387 + 0.9092974268256816954j))
    assert ae(fp.expj(0.75), (0.73168886887382088631 + 0.68163876002333416673j))
    assert ae(fp.expj(2+3j), (-0.020718731002242879378 + 0.045271253156092975488j))
    assert ae(fp.expjpi(0), (1.0 + 0.0j))
    assert ae(fp.expjpi(1), (-1.0 + 0.0j))
    assert ae(fp.expjpi(2), (1.0 + 0.0j))
    assert ae(fp.expjpi(0.75), (-0.7071067811865475244 + 0.7071067811865475244j))
    assert ae(fp.expjpi(2+3j), (0.000080699517570304599239 + 0.0j))

