
def _two_loop_recursion(state: LBFGSResults):
  dtype = state.rho_history.dtype
  his_size = len(state.rho_history)
  curr_size = jnp.where(state.k < his_size, state.k, his_size)
  q = -jnp.conj(state.g_k)
  a_his = jnp.zeros_like(state.rho_history)

  def body_fun1(j, carry):
    i = his_size - 1 - j
    _q, _a_his = carry
    a_i = state.rho_history[i] * _dot(jnp.conj(state.s_history[i]), _q).real.astype(dtype)
    _a_his = _a_his.at[i].set(a_i)
    _q = _q - a_i * jnp.conj(state.y_history[i])
    return _q, _a_his

  q, a_his = lax.fori_loop(0, curr_size, body_fun1, (q, a_his))
  q = state.gamma * q

  def body_fun2(j, _q):
    i = his_size - curr_size + j
    b_i = state.rho_history[i] * _dot(state.y_history[i], _q).real.astype(dtype)
    _q = _q + (a_his[i] - b_i) * state.s_history[i]
    return _q

  q = lax.fori_loop(0, curr_size, body_fun2, q)
  return q

