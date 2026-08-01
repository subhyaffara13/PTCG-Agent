
def create_block(typestr, placement, item_shape=None, num_offset=0, maker=new_block):
    """
    Supported typestr:

        * float, f8, f4, f2
        * int, i8, i4, i2, i1
        * uint, u8, u4, u2, u1
        * complex, c16, c8
        * bool
        * object, string, O
        * datetime, dt, M8[ns], M8[ns, tz]
        * timedelta, td, m8[ns]
        * sparse (SparseArray with fill_value=0.0)
        * sparse_na (SparseArray with fill_value=np.nan)
        * category, category2

    """
    placement = BlockPlacement(placement)
    num_items = len(placement)

    if item_shape is None:
        item_shape = (N,)

    shape = (num_items, *item_shape)

    mat = get_numeric_mat(shape)

    if typestr in (
        "float",
        "f8",
        "f4",
        "f2",
        "int",
        "i8",
        "i4",
        "i2",
        "i1",
        "uint",
        "u8",
        "u4",
        "u2",
        "u1",
    ):
        values = mat.astype(typestr) + num_offset
    elif typestr in ("complex", "c16", "c8"):
        values = 1.0j * (mat.astype(typestr) + num_offset)
    elif typestr in ("object", "string", "O"):
        values = np.reshape([f"A{i:d}" for i in mat.ravel() + num_offset], shape)
    elif typestr in ("b", "bool"):
        values = np.ones(shape, dtype=np.bool_)
    elif typestr in ("datetime", "dt", "M8[ns]"):
        values = (mat * 1e9).astype("M8[ns]")
    elif typestr.startswith("M8[ns"):
        # datetime with tz
        m = re.search(r"M8\[ns,\s*(\w+\/?\w*)\]", typestr)
        assert m is not None, f"incompatible typestr -> {typestr}"
        tz = m.groups()[0]
        assert num_items == 1, "must have only 1 num items for a tz-aware"
        values = DatetimeIndex(np.arange(N) * 10**9, tz=tz)._data
        values = ensure_block_shape(values, ndim=len(shape))
    elif typestr in ("timedelta", "td", "m8[ns]"):
        values = (mat * 1).astype("m8[ns]")
    elif typestr in ("category",):
        values = Categorical([1, 1, 2, 2, 3, 3, 3, 3, 4, 4])
    elif typestr in ("category2",):
        values = Categorical(["a", "a", "a", "a", "b", "b", "c", "c", "c", "d"])
    elif typestr in ("sparse", "sparse_na"):
        if shape[-1] != 10:
            # We also are implicitly assuming this in the category cases above
            raise NotImplementedError

        assert all(s == 1 for s in shape[:-1])
        if typestr.endswith("_na"):
            fill_value = np.nan
        else:
            fill_value = 0.0
        values = SparseArray(
            [fill_value, fill_value, 1, 2, 3, fill_value, 4, 5, fill_value, 6],
            fill_value=fill_value,
        )
        arr = values.sp_values.view()
        arr += num_offset - 1
    else:
        raise ValueError(f'Unsupported typestr: "{typestr}"')

    values = maybe_coerce_values(values)
    return maker(values, placement=placement, ndim=len(shape))

