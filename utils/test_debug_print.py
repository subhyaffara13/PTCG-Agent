
def test_debug_print(capfd):
    """
    Matches the expected output of a debug print with the actual output.
    Note that the iterator dump should not be considered stable API,
    this test is mainly to ensure the print does not crash.

    Currently uses a subprocess to avoid dealing with the C level `printf`s.
    """
    # the expected output with all addresses and sizes stripped (they vary
    # and/or are platform dependent).
    expected = """
    ------ BEGIN ITERATOR DUMP ------
    | Iterator Address:
    | ItFlags: BUFFER REDUCE
    | NDim: 2
    | NOp: 2
    | IterSize: 50
    | IterStart: 0
    | IterEnd: 50
    | IterIndex: 0
    | Iterator SizeOf:
    | BufferData SizeOf:
    | AxisData SizeOf:
    |
    | Perm: 0 1
    | DTypes:
    | DTypes: dtype('float64') dtype('int32')
    | InitDataPtrs:
    | BaseOffsets: 0 0
    | Ptrs:
    | User/buffer ptrs:
    | Operands:
    | Operand DTypes: dtype('int64') dtype('float64')
    | OpItFlags:
    |   Flags[0]: READ CAST
    |   Flags[1]: READ WRITE CAST REDUCE
    |
    | BufferData:
    |   BufferSize: 50
    |   Size: 5
    |   BufIterEnd: 5
    |   BUFFER CoreSize: 5
    |   REDUCE Pos: 0
    |   REDUCE OuterSize: 10
    |   REDUCE OuterDim: 1
    |   Strides: 8 4
    |   REDUCE Outer Strides: 40 0
    |   REDUCE Outer Ptrs:
    |   ReadTransferFn:
    |   ReadTransferData:
    |   WriteTransferFn:
    |   WriteTransferData:
    |   Buffers:
    |
    | AxisData[0]:
    |   Shape: 5
    |   Index: 0
    |   Strides: 16 8
    | AxisData[1]:
    |   Shape: 10
    |   Index: 0
    |   Strides: 80 0
    ------- END ITERATOR DUMP -------
    """.strip().splitlines()

    arr1 = np.arange(100, dtype=np.int64).reshape(10, 10)[:, ::2]
    arr2 = np.arange(5.)
    it = np.nditer((arr1, arr2), op_dtypes=["d", "i4"], casting="unsafe",
                   flags=["reduce_ok", "buffered"],
                   op_flags=[["readonly"], ["readwrite"]])
    it.debug_print()
    res = capfd.readouterr().out
    res = res.strip().splitlines()

    assert len(res) == len(expected)
    for res_line, expected_line in zip(res, expected):
        # The actual output may have additional pointers listed that are
        # stripped from the example output:
        assert res_line.startswith(expected_line.strip())

