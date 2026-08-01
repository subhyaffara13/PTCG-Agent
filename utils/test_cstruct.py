
def test_cstruct(get_module):

    class data_source:
        """
        This class is for testing the timing of the PyCapsule destructor
        invoked when numpy release its reference to the shared data as part of
        the numpy array interface protocol. If the PyCapsule destructor is
        called early the shared data is freed and invalid memory accesses will
        occur.
        """

        def __init__(self, size, value):
            self.size = size
            self.value = value

        @property
        def __array_struct__(self):
            return get_module.new_array_struct(self.size, self.value)

    # write to the same stream as the C code
    stderr = sys.__stderr__

    # used to validate the shared data.
    expected_value = -3.1415
    multiplier = -10000.0

    # create some data to share with numpy via the array interface
    # assign the data an expected value.
    stderr.write(' ---- create an object to share data ---- \n')
    buf = data_source(256, expected_value)
    stderr.write(' ---- OK!\n\n')

    # share the data
    stderr.write(' ---- share data via the array interface protocol ---- \n')
    arr = np.array(buf, copy=False)
    stderr.write(f'arr.__array_interface___ = {str(arr.__array_interface__)}\n')
    stderr.write(f'arr.base = {str(arr.base)}\n')
    stderr.write(' ---- OK!\n\n')

    # release the source of the shared data. this will not release the data
    # that was shared with numpy, that is done in the PyCapsule destructor.
    stderr.write(' ---- destroy the object that shared data ---- \n')
    buf = None
    stderr.write(' ---- OK!\n\n')

    # check that we got the expected data. If the PyCapsule destructor we
    # defined was prematurely called then this test will fail because our
    # destructor sets the elements of the array to NaN before free'ing the
    # buffer. Reading the values here may also cause a SEGV
    assert np.allclose(arr, expected_value)

    # read the data. If the PyCapsule destructor we defined was prematurely
    # called then reading the values here may cause a SEGV and will be reported
    # as invalid reads by valgrind
    stderr.write(' ---- read shared data ---- \n')
    stderr.write(f'arr = {str(arr)}\n')
    stderr.write(' ---- OK!\n\n')

    # write to the shared buffer. If the shared data was prematurely deleted
    # this will may cause a SEGV and valgrind will report invalid writes
    stderr.write(' ---- modify shared data ---- \n')
    arr *= multiplier
    expected_value *= multiplier
    stderr.write(f'arr.__array_interface___ = {str(arr.__array_interface__)}\n')
    stderr.write(f'arr.base = {str(arr.base)}\n')
    stderr.write(' ---- OK!\n\n')

    # read the data. If the shared data was prematurely deleted this
    # will may cause a SEGV and valgrind will report invalid reads
    stderr.write(' ---- read modified shared data ---- \n')
    stderr.write(f'arr = {str(arr)}\n')
    stderr.write(' ---- OK!\n\n')

    # check that we got the expected data. If the PyCapsule destructor we
    # defined was prematurely called then this test will fail because our
    # destructor sets the elements of the array to NaN before free'ing the
    # buffer. Reading the values here may also cause a SEGV
    assert np.allclose(arr, expected_value)

    # free the shared data, the PyCapsule destructor should run here
    stderr.write(' ---- free shared data ---- \n')
    arr = None
    stderr.write(' ---- OK!\n\n')

