
def _dct2(x: Array, axes: Sequence[int], norm: str | None) -> Array:
  axis1, axis2 = map(partial(canonicalize_axis, num_dims=x.ndim), axes)
  N1, N2 = x.shape[axis1], x.shape[axis2]
  v = _dct_interleave(_dct_interleave(x, axis1), axis2)
  V = jnp_fft.fftn(v, axes=axes)
  k1 = lax.expand_dims(jnp.arange(N1, dtype=V.dtype),
                       [a for a in range(x.ndim) if a != axis1])
  k2 = lax.expand_dims(jnp.arange(N2, dtype=V.dtype),
                       [a for a in range(x.ndim) if a != axis2])
  out = _W4(N1, k1) * (_W4(N2, k2) * V + _W4(N2, -k2) * jnp.roll(jnp.flip(V, axis=axis2), shift=1, axis=axis2))
  out = 2 * out.real
  if norm == 'ortho':
    return _dct_ortho_norm(_dct_ortho_norm(out, axis1), axis2)
  return out

