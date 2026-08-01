
def test_maybe_promote_any_numpy_dtype_with_na(any_numpy_dtype, nulls_fixture):
    fill_value = nulls_fixture
    dtype = np.dtype(any_numpy_dtype)

    if isinstance(fill_value, Decimal):
        # Subject to change, but ATM (When Decimal(NAN) is being added to nulls_fixture)
        #  this is the existing behavior in maybe_promote,
        #  hinges on is_valid_na_for_dtype
        if dtype.kind in "iufc":
            if dtype.kind in "iu":
                expected_dtype = np.dtype(np.float64)
            else:
                expected_dtype = dtype
            exp_val_for_scalar = np.nan
        else:
            expected_dtype = np.dtype(object)
            exp_val_for_scalar = fill_value
    elif dtype.kind in "iu" and fill_value is not NaT:
        # integer + other missing value (np.nan / None) casts to float
        expected_dtype = np.float64
        exp_val_for_scalar = np.nan
    elif dtype == object and fill_value is NaT:
        # inserting into object does not cast the value
        # but *does* cast None to np.nan
        expected_dtype = np.dtype(object)
        exp_val_for_scalar = fill_value
    elif dtype.kind in "mM":
        # datetime / timedelta cast all missing values to dtyped-NaT
        expected_dtype = dtype
        exp_val_for_scalar = dtype.type("NaT", "ns")
    elif fill_value is NaT:
        # NaT upcasts everything that's not datetime/timedelta to object
        expected_dtype = np.dtype(object)
        exp_val_for_scalar = NaT
    elif dtype.kind in "fc":
        # float / complex + missing value (!= NaT) stays the same
        expected_dtype = dtype
        exp_val_for_scalar = np.nan
    else:
        # all other cases cast to object, and use np.nan as missing value
        expected_dtype = np.dtype(object)
        if fill_value is pd.NA:
            exp_val_for_scalar = pd.NA
        else:
            exp_val_for_scalar = np.nan

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

