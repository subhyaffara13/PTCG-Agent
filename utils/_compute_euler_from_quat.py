
def _compute_euler_from_quat(quat: Array, axes: Array, extrinsic: bool, degrees: bool) -> Array:
  angle_first = jnp.where(extrinsic, 0, 2)
  angle_third = jnp.where(extrinsic, 2, 0)
  axes = jnp.where(extrinsic, axes, axes[::-1])
  i = axes[0]
  j = axes[1]
  k = axes[2]
  symmetric = i == k
  k = jnp.where(symmetric, 3 - i - j, k)
  sign = jnp.array((i - j) * (j - k) * (k - i) // 2, dtype=quat.dtype)
  eps = 1e-7
  a = jnp.where(symmetric, quat[3], quat[3] - quat[j])
  b = jnp.where(symmetric, quat[i], quat[i] + quat[k] * sign)
  c = jnp.where(symmetric, quat[j], quat[j] + quat[3])
  d = jnp.where(symmetric, quat[k] * sign, quat[k] * sign - quat[i])
  angles = jnp.empty(3, dtype=quat.dtype)
  angles = angles.at[1].set(2 * jnp.arctan2(jnp.hypot(c, d), jnp.hypot(a, b)))
  case = jnp.where(jnp.abs(angles[1] - np.pi) <= eps, 2, 0)
  case = jnp.where(jnp.abs(angles[1]) <= eps, 1, case)
  half_sum = jnp.arctan2(b, a)
  half_diff = jnp.arctan2(d, c)
  angles = angles.at[0].set(jnp.where(case == 1, 2 * half_sum, 2 * half_diff * jnp.where(extrinsic, -1, 1)))  # any degenerate case
  angles = angles.at[angle_first].set(jnp.where(case == 0, half_sum - half_diff, angles[angle_first]))
  angles = angles.at[angle_third].set(jnp.where(case == 0, half_sum + half_diff, angles[angle_third]))
  angles = angles.at[angle_third].set(jnp.where(symmetric, angles[angle_third], angles[angle_third] * sign))
  angles = angles.at[1].set(jnp.where(symmetric, angles[1], angles[1] - np.pi / 2))
  angles = (angles + np.pi) % (2 * np.pi) - np.pi
  return jnp.where(degrees, jnp.rad2deg(angles), angles)

