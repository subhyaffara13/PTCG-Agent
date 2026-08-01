
def _type_promotion_lattice(strict: bool, x64: bool) -> dict[JAXType, list[JAXType]]:
  """
  Return the type promotion lattice in the form of a DAG.
  This DAG maps each type to its immediately higher types on the lattice.

  Args:
    strict: use strict promotion lattice?
    x64: allow promotions that form x64 types from non-x64 inputs?
  """
  b1, = _bool_types
  u1, i1 = None, None
  if _int1_dtype is not None:
    assert _uint1_dtype is not None
    u1, u2, u4, u8, u16, u32, u64, i1, i2, i4, i8, i16, i32, i64 = _int_types
  else:
    u2, u4, u8, u16, u32, u64, i2, i4, i8, i16, i32, i64 = _int_types
  *small_float_types, bf16, f16, f32, f64 = _float_types
  c64, c128 = _complex_types
  i_, f_, c_ = _weak_types
  if not strict:
    out: dict[JAXType, list[JAXType]] = {
        b1: [i_],
        i_: [u8, u2, u4, i8, i2, i4],
        u2: [],
        u4: [],
        u8: [i16, u16],
        u16: [i32, u32],
        u32: [i64, u64],
        u64: [f_],
        i2: [],
        i4: [],
        i8: [i16],
        i16: [i32],
        i32: [i64],
        i64: [f_],
        f_: [*small_float_types, bf16, f16, c_],
        **{t: [] for t in small_float_types},
        bf16: [f32],
        f16: [f32],
        f32: [f64, c64],
        f64: [c128],
        c_: [c64],
        c64: [c128],
        c128: [],
    }
    if i1 is not None:
      out[i_].append(i1)
      out[i1] = []
    if u1 is not None:
      out[i_].append(u1)
      out[u1] = []
    # If x64 mode is not enabled, then we want to avoid any promotions that form
    # 64-bit types from non-64-bit inputs. There's only one of these in the
    # entire promotion lattice, namely u4xi4->i8, which we can avoid by
    # replacing it with u4xi4->i4.
    if not x64:
      out[u32] = [i32, u64]
    return out
  else:
    return {
      i_: [f_] + _int_types,
      f_: [c_] + _float_types,
      c_: _complex_types,
      **{t: [] for t in _jax_types}
    }

