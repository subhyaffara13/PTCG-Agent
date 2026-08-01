
def test_is_categorical_dtype():
    msg = "is_categorical_dtype is deprecated"
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        assert not com.is_categorical_dtype(object)
        assert not com.is_categorical_dtype([1, 2, 3])

        assert com.is_categorical_dtype(CategoricalDtype())
        assert com.is_categorical_dtype(pd.Categorical([1, 2, 3]))
        assert com.is_categorical_dtype(pd.CategoricalIndex([1, 2, 3]))

