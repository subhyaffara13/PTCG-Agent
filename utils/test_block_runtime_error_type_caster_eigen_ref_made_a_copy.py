
def test_block_runtime_error_type_caster_eigen_ref_made_a_copy():
    with pytest.raises(RuntimeError) as excinfo:
        m.block(ref, 0, 0, 0, 0)
    assert str(excinfo.value) == "type_caster for Eigen::Ref made a copy."

