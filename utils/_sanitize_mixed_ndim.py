
def _sanitize_mixed_ndim(
    objs: list[Series | DataFrame],
    sample: Series | DataFrame,
    ignore_index: bool,
    axis: AxisInt,
) -> list[Series | DataFrame]:
    # if we have mixed ndims, then convert to highest ndim
    # creating column numbers as needed

    new_objs = []

    current_column = 0
    max_ndim = sample.ndim
    for obj in objs:
        ndim = obj.ndim
        if ndim == max_ndim:
            pass

        elif ndim != max_ndim - 1:
            raise ValueError(
                "cannot concatenate unaligned mixed dimensional NDFrame objects"
            )

        else:
            name = getattr(obj, "name", None)
            rename_columns = False
            if ignore_index or name is None:
                if axis == 1:
                    # doing a row-wise concatenation so need everything
                    # to line up
                    if name is None:
                        name = 0
                        rename_columns = True
                # doing a column-wise concatenation so need series
                # to have unique names
                elif name is None:
                    rename_columns = True
                    name = current_column
                    current_column += 1
                obj = sample._constructor(obj, copy=False)
                if isinstance(obj, ABCDataFrame) and rename_columns:
                    obj.columns = range(name, name + 1, 1)
            else:
                obj = sample._constructor({name: obj}, copy=False)

        new_objs.append(obj)

    return new_objs

