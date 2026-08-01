
def test_dense_signature(doc):
    assert (
        doc(m.double_col)
        == """
        double_col(arg0: numpy.ndarray[numpy.float32[m, 1]]) -> numpy.ndarray[numpy.float32[m, 1]]
    """
    )
    assert (
        doc(m.double_row)
        == """
        double_row(arg0: numpy.ndarray[numpy.float32[1, n]]) -> numpy.ndarray[numpy.float32[1, n]]
    """
    )
    assert doc(m.double_complex) == (
        """
        double_complex(arg0: numpy.ndarray[numpy.complex64[m, 1]])"""
        """ -> numpy.ndarray[numpy.complex64[m, 1]]
    """
    )
    assert doc(m.double_mat_rm) == (
        """
        double_mat_rm(arg0: numpy.ndarray[numpy.float32[m, n]])"""
        """ -> numpy.ndarray[numpy.float32[m, n]]
    """
    )

