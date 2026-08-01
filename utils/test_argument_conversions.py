
def test_argument_conversions(forcecast, contiguity, noconvert):
    function_name = "accept_double"
    if contiguity == "C":
        function_name += "_c_style"
    elif contiguity == "F":
        function_name += "_f_style"
    if forcecast:
        function_name += "_forcecast"
    if noconvert:
        function_name += "_noconvert"
    function = getattr(m, function_name)

    for dtype in [np.dtype("float32"), np.dtype("float64"), np.dtype("complex128")]:
        for order in ["C", "F"]:
            for shape in [(2, 2), (1, 3, 1, 1), (1, 1, 1), (0,)]:
                if not noconvert:
                    # If noconvert is not passed, only complex128 needs to be truncated and
                    # "cannot be safely obtained". So without `forcecast`, the argument shouldn't
                    # be accepted.
                    should_raise = dtype.name == "complex128" and not forcecast
                else:
                    # If noconvert is passed, only float64 and the matching order is accepted.
                    # If at most one dimension has a size greater than 1, the array is also
                    # trivially contiguous.
                    trivially_contiguous = sum(1 for d in shape if d > 1) <= 1
                    should_raise = dtype.name != "float64" or (
                        contiguity is not None
                        and contiguity != order
                        and not trivially_contiguous
                    )

                array = np.zeros(shape, dtype=dtype, order=order)
                if not should_raise:
                    function(array)
                else:
                    with pytest.raises(
                        TypeError, match="incompatible function arguments"
                    ):
                        function(array)

