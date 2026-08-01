
def _threefry4x32_lowering(k0, k1, k2, k3, x0, x1, x2, x3):
  """Apply the Threefry 4x32 hash with 20 rounds.

  Args:
    k0: uint32 array forming the first part of the key.
    k1: uint32 array forming the second part of the key.
    k2: uint32 array forming the third part of the key.
    k3: uint32 array forming the fourth part of the key.
    x0: uint32 array forming the first part of the counter/input.
    x1: uint32 array forming the second part of the counter/input.
    x2: uint32 array forming the third part of the counter/input.
    x3: uint32 array forming the fourth part of the counter/input.

  Returns:
    A tuple of four uint32 arrays (out0, out1, out2, out3).
  """
  # Key schedule: ks[i] = k[i], ks[4] = k0 ^ k1 ^ k2 ^ k3 ^ parity
  ks = [k0, k1, k2, k3, k0 ^ k1 ^ k2 ^ k3 ^ _SKEIN_KS_PARITY32]

  # Initial key injection
  x0 = x0 + ks[0]
  x1 = x1 + ks[1]
  x2 = x2 + ks[2]
  x3 = x3 + ks[3]

  for rnd in range(_DEFAULT_ROUNDS):
    rot0 = _ROTATIONS_32X4[rnd % 8, 0]
    rot1 = _ROTATIONS_32X4[rnd % 8, 1]

    if (rnd % 2) == 0:
      # Even sub-round: mix (0,1) and (2,3)
      x0 = x0 + x1
      x1 = _rotate_left_u32(x1, rot0)
      x1 = x0 ^ x1
      x2 = x2 + x3
      x3 = _rotate_left_u32(x3, rot1)
      x3 = x2 ^ x3
    else:
      # Odd sub-round: mix (0,3) and (2,1) — the 4-word permutation
      x0 = x0 + x3
      x3 = _rotate_left_u32(x3, rot0)
      x3 = x0 ^ x3
      x2 = x2 + x1
      x1 = _rotate_left_u32(x1, rot1)
      x1 = x2 ^ x1

    # Key injection every 4 rounds
    if (rnd & 3) == 3:
      inject_idx = rnd // 4
      x0 = x0 + ks[(1 + inject_idx) % 5]
      x1 = x1 + ks[(2 + inject_idx) % 5]
      x2 = x2 + ks[(3 + inject_idx) % 5]
      x3 = x3 + ks[(4 + inject_idx) % 5]
      x3 = x3 + np.uint32(1 + inject_idx)

  return (x0, x1, x2, x3)

