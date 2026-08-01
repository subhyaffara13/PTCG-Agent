
def categorical_order(vector, order=None):
    """Return a list of unique data values.

    Determine an ordered list of levels in ``values``.

    Parameters
    ----------
    vector : list, array, Categorical, or Series
        Vector of "categorical" values
    order : list-like, optional
        Desired order of category levels to override the order determined
        from the ``values`` object.

    Returns
    -------
    order : list
        Ordered list of category levels not including null values.

    """
    if order is None:
        if hasattr(vector, "categories"):
            order = vector.categories
        else:
            try:
                order = vector.cat.categories
            except (TypeError, AttributeError):

                order = pd.Series(vector).unique()

                if variable_type(vector) == "numeric":
                    order = np.sort(order)

        order = filter(pd.notnull, order)
    return list(order)


def categorical_order(vector: Series, order: list | None = None) -> list:
    """
    Return a list of unique data values using seaborn's ordering rules.

    Parameters
    ----------
    vector : Series
        Vector of "categorical" values
    order : list
        Desired order of category levels to override the order determined
        from the `data` object.

    Returns
    -------
    order : list
        Ordered list of category levels not including null values.

    """
    if order is not None:
        return order

    if vector.dtype.name == "category":
        order = list(vector.cat.categories)
    else:
        order = list(filter(pd.notnull, vector.unique()))
        if variable_type(pd.Series(order)) == "numeric":
            order.sort()

    return order

