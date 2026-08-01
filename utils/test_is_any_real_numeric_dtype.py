
def test_is_any_real_numeric_dtype():
    assert not com.is_any_real_numeric_dtype(str)
    assert not com.is_any_real_numeric_dtype(bool)
    assert not com.is_any_real_numeric_dtype(complex)
    assert not com.is_any_real_numeric_dtype(object)
    assert not com.is_any_real_numeric_dtype(np.datetime64)
    assert not com.is_any_real_numeric_dtype(np.array(["a", "b", complex(1, 2)]))
    assert not com.is_any_real_numeric_dtype(pd.DataFrame([complex(1, 2), True]))

    assert com.is_any_real_numeric_dtype(int)
    assert com.is_any_real_numeric_dtype(float)
    assert com.is_any_real_numeric_dtype(np.array([1, 2.5]))

