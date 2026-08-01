
def test_hashable_tuple_args():
    # require that the elements of such tuples are themselves hashable

    df3 = DataFrame(
        {
            "data": [
                (
                    1,
                    [],
                ),
                (
                    2,
                    {},
                ),
            ]
        }
    )
    with pytest.raises(TypeError, match="unhashable type: 'list'"):
        hash_pandas_object(df3)

