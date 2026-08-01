
def test_overload_resolution(msg):
    # Exact overload matches:
    assert m.overloaded(np.array([1], dtype="float64")) == "double"
    assert m.overloaded(np.array([1], dtype="float32")) == "float"
    assert m.overloaded(np.array([1], dtype="ushort")) == "unsigned short"
    assert m.overloaded(np.array([1], dtype="intc")) == "int"
    assert m.overloaded(np.array([1], dtype="longlong")) == "long long"
    assert m.overloaded(np.array([1], dtype="complex")) == "double complex"
    assert m.overloaded(np.array([1], dtype="csingle")) == "float complex"

    # No exact match, should call first convertible version:
    assert m.overloaded(np.array([1], dtype="uint8")) == "double"

    with pytest.raises(TypeError) as excinfo:
        m.overloaded("not an array")
    assert (
        msg(excinfo.value)
        == """
        overloaded(): incompatible function arguments. The following argument types are supported:
            1. (arg0: numpy.ndarray[numpy.float64]) -> str
            2. (arg0: numpy.ndarray[numpy.float32]) -> str
            3. (arg0: numpy.ndarray[numpy.int32]) -> str
            4. (arg0: numpy.ndarray[numpy.uint16]) -> str
            5. (arg0: numpy.ndarray[numpy.int64]) -> str
            6. (arg0: numpy.ndarray[numpy.complex128]) -> str
            7. (arg0: numpy.ndarray[numpy.complex64]) -> str

        Invoked with: 'not an array'
    """
    )

    assert m.overloaded2(np.array([1], dtype="float64")) == "double"
    assert m.overloaded2(np.array([1], dtype="float32")) == "float"
    assert m.overloaded2(np.array([1], dtype="complex64")) == "float complex"
    assert m.overloaded2(np.array([1], dtype="complex128")) == "double complex"
    assert m.overloaded2(np.array([1], dtype="float32")) == "float"

    assert m.overloaded3(np.array([1], dtype="float64")) == "double"
    assert m.overloaded3(np.array([1], dtype="intc")) == "int"
    expected_exc = """
        overloaded3(): incompatible function arguments. The following argument types are supported:
            1. (arg0: numpy.ndarray[numpy.int32]) -> str
            2. (arg0: numpy.ndarray[numpy.float64]) -> str

        Invoked with: """

    with pytest.raises(TypeError) as excinfo:
        m.overloaded3(np.array([1], dtype="uintc"))
    assert msg(excinfo.value) == expected_exc + repr(np.array([1], dtype="uint32"))
    with pytest.raises(TypeError) as excinfo:
        m.overloaded3(np.array([1], dtype="float32"))
    assert msg(excinfo.value) == expected_exc + repr(np.array([1.0], dtype="float32"))
    with pytest.raises(TypeError) as excinfo:
        m.overloaded3(np.array([1], dtype="complex"))
    assert msg(excinfo.value) == expected_exc + repr(np.array([1.0 + 0.0j]))

    # Exact matches:
    assert m.overloaded4(np.array([1], dtype="double")) == "double"
    assert m.overloaded4(np.array([1], dtype="longlong")) == "long long"
    # Non-exact matches requiring conversion.  Since float to integer isn't a
    # save conversion, it should go to the double overload, but short can go to
    # either (and so should end up on the first-registered, the long long).
    assert m.overloaded4(np.array([1], dtype="float32")) == "double"
    assert m.overloaded4(np.array([1], dtype="short")) == "long long"

    assert m.overloaded5(np.array([1], dtype="double")) == "double"
    assert m.overloaded5(np.array([1], dtype="uintc")) == "unsigned int"
    assert m.overloaded5(np.array([1], dtype="float32")) == "unsigned int"

