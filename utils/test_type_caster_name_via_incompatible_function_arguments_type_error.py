
def test_type_caster_name_via_incompatible_function_arguments_type_error():
    with pytest.raises(TypeError, match=r"1\. \(arg0: object, arg1: int\) -> None"):
        m.pass_pyobject_ptr_and_int(ValueHolder(101), ValueHolder(202))

