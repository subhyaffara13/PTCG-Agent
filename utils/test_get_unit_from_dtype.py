
def test_get_unit_from_dtype():
    # datetime64
    assert py_get_unit_from_dtype(np.dtype("M8[Y]")) == NpyDatetimeUnit.NPY_FR_Y.value
    assert py_get_unit_from_dtype(np.dtype("M8[M]")) == NpyDatetimeUnit.NPY_FR_M.value
    assert py_get_unit_from_dtype(np.dtype("M8[W]")) == NpyDatetimeUnit.NPY_FR_W.value
    # B has been deprecated and removed -> no 3
    assert py_get_unit_from_dtype(np.dtype("M8[D]")) == NpyDatetimeUnit.NPY_FR_D.value
    assert py_get_unit_from_dtype(np.dtype("M8[h]")) == NpyDatetimeUnit.NPY_FR_h.value
    assert py_get_unit_from_dtype(np.dtype("M8[m]")) == NpyDatetimeUnit.NPY_FR_m.value
    assert py_get_unit_from_dtype(np.dtype("M8[s]")) == NpyDatetimeUnit.NPY_FR_s.value
    assert py_get_unit_from_dtype(np.dtype("M8[ms]")) == NpyDatetimeUnit.NPY_FR_ms.value
    assert py_get_unit_from_dtype(np.dtype("M8[us]")) == NpyDatetimeUnit.NPY_FR_us.value
    assert py_get_unit_from_dtype(np.dtype("M8[ns]")) == NpyDatetimeUnit.NPY_FR_ns.value
    assert py_get_unit_from_dtype(np.dtype("M8[ps]")) == NpyDatetimeUnit.NPY_FR_ps.value
    assert py_get_unit_from_dtype(np.dtype("M8[fs]")) == NpyDatetimeUnit.NPY_FR_fs.value
    assert py_get_unit_from_dtype(np.dtype("M8[as]")) == NpyDatetimeUnit.NPY_FR_as.value

    # timedelta64
    assert py_get_unit_from_dtype(np.dtype("m8[Y]")) == NpyDatetimeUnit.NPY_FR_Y.value
    assert py_get_unit_from_dtype(np.dtype("m8[M]")) == NpyDatetimeUnit.NPY_FR_M.value
    assert py_get_unit_from_dtype(np.dtype("m8[W]")) == NpyDatetimeUnit.NPY_FR_W.value
    # B has been deprecated and removed -> no 3
    assert py_get_unit_from_dtype(np.dtype("m8[D]")) == NpyDatetimeUnit.NPY_FR_D.value
    assert py_get_unit_from_dtype(np.dtype("m8[h]")) == NpyDatetimeUnit.NPY_FR_h.value
    assert py_get_unit_from_dtype(np.dtype("m8[m]")) == NpyDatetimeUnit.NPY_FR_m.value
    assert py_get_unit_from_dtype(np.dtype("m8[s]")) == NpyDatetimeUnit.NPY_FR_s.value
    assert py_get_unit_from_dtype(np.dtype("m8[ms]")) == NpyDatetimeUnit.NPY_FR_ms.value
    assert py_get_unit_from_dtype(np.dtype("m8[us]")) == NpyDatetimeUnit.NPY_FR_us.value
    assert py_get_unit_from_dtype(np.dtype("m8[ns]")) == NpyDatetimeUnit.NPY_FR_ns.value
    assert py_get_unit_from_dtype(np.dtype("m8[ps]")) == NpyDatetimeUnit.NPY_FR_ps.value
    assert py_get_unit_from_dtype(np.dtype("m8[fs]")) == NpyDatetimeUnit.NPY_FR_fs.value
    assert py_get_unit_from_dtype(np.dtype("m8[as]")) == NpyDatetimeUnit.NPY_FR_as.value

