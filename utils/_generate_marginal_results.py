
def _generate_marginal_results(
    table,
    data: DataFrame,
    values,
    rows,
    cols,
    aggfunc,
    kwargs,
    observed: bool,
    margins_name: Hashable = "All",
    dropna: bool = True,
):
    margin_keys: list | Index
    if len(cols) > 0:
        # need to "interleave" the margins
        table_pieces = []
        margin_keys = []

        def _all_key(key):
            return (key, margins_name) + ("",) * (len(cols) - 1)

        if len(rows) > 0:
            margin = (
                data[rows + values]
                .groupby(rows, observed=observed, dropna=dropna)
                .agg(aggfunc, **kwargs)
            )
            cat_axis = 1

            for key, piece in table.T.groupby(level=0, observed=observed):
                piece = piece.T
                all_key = _all_key(key)

                piece[all_key] = margin[key]

                table_pieces.append(piece)
                margin_keys.append(all_key)
        else:
            margin = (
                data[cols[:1] + values]
                .groupby(cols[:1], observed=observed, dropna=dropna)
                .agg(aggfunc, **kwargs)
                .T
            )

            cat_axis = 0
            for key, piece in table.groupby(level=0, observed=observed):
                if len(cols) > 1:
                    all_key = _all_key(key)
                else:
                    all_key = margins_name
                table_pieces.append(piece)
                transformed_piece = margin[key].to_frame().T
                if isinstance(piece.index, MultiIndex):
                    # We are adding an empty level
                    transformed_piece.index = MultiIndex.from_tuples(
                        [all_key],
                        names=[*piece.index.names, None],
                    )
                else:
                    transformed_piece.index = Index([all_key], name=piece.index.name)

                # append piece for margin into table_piece
                table_pieces.append(transformed_piece)
                margin_keys.append(all_key)

        if not table_pieces:
            # GH 49240
            return table
        else:
            result = concat(table_pieces, axis=cat_axis)

        if len(rows) == 0:
            return result
    else:
        result = table
        margin_keys = table.columns

    if len(cols) > 0:
        row_margin = (
            data[cols + values]
            .groupby(cols, observed=observed, dropna=dropna)
            .agg(aggfunc, **kwargs)
        )
        row_margin = row_margin.stack()

        # GH#26568. Use names instead of indices in case of numeric names
        new_order_indices = itertools.chain([len(cols)], range(len(cols)))
        new_order_names = [row_margin.index.names[i] for i in new_order_indices]
        row_margin.index = row_margin.index.reorder_levels(new_order_names)
    else:
        row_margin = data._constructor_sliced(np.nan, index=result.columns)

    return result, margin_keys, row_margin

