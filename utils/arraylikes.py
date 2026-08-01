
def arraylikes():
    """Test parameters for functions converting an array into various array-likes."""

    params = []

    # base array:
    def ndarray(a):
        return a

    params.append(param(ndarray, id="ndarray"))

    # subclass:
    class MyArr(np.ndarray):
        pass

    def subclass(a):
        return a.view(MyArr)

    params.append(subclass)

    class _SequenceLike:
        # Older NumPy versions, sometimes cared whether a protocol array was
        # also _SequenceLike.  This shouldn't matter, but keep it for now
        # for __array__ and not the others.
        def __len__(self):
            raise TypeError

        def __getitem__(self, _, /):
            raise TypeError

    # Array-interface
    class ArrayDunder(_SequenceLike):
        def __init__(self, a):
            self.a = a

        def __array__(self, dtype=None, copy=None):
            if dtype is None:
                return self.a
            return self.a.astype(dtype)

    params.append(param(ArrayDunder, id="__array__"))

    # memory-view
    params.append(param(memoryview, id="memoryview"))

    # Array-interface
    class ArrayInterface:
        def __init__(self, a):
            self.a = a  # need to hold on to keep interface valid
            self.__array_interface__ = a.__array_interface__

    params.append(param(ArrayInterface, id="__array_interface__"))

    # Array-Struct
    class ArrayStruct:
        def __init__(self, a):
            self.a = a  # need to hold on to keep struct valid
            self.__array_struct__ = a.__array_struct__

    params.append(param(ArrayStruct, id="__array_struct__"))

    return params

