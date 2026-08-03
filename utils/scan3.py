from typing import Callable

def scan3(f: Callable[[Carry, X], tuple[Carry, Y]],
         init: Carry,
         xs: X | None = None,
         length: int | None = None,
         reverse: bool = False,
         unroll: int | bool = 1,
         _split_transpose: bool = False) -> tuple[Carry, Y]:
  init_flat = FlatTree.flatten(init)
  carry_avals = init_flat.map(typeof)
  carry_refs = [core.new_ref(x) for x in init_flat]

  def read_carry():
    return carry_avals.update([r[...] for r in carry_refs]).unflatten()

  def write_carry(val):
    carry_flat = FlatTree.flatten(val)
    assert carry_flat.tree == init_flat.tree  # TODO: better error
    for ref, c in zip(carry_refs, carry_flat):
      ref[...] = c

  def body_no_carry(x):
    carry, y = f(read_carry(), x)
    write_carry(carry)
    return y

  ys = scan_nocarry(
      body_no_carry, xs,
      length=length, reverse=reverse, unroll=unroll)
  return read_carry(), ys

