
def diff_types(dbg, new_leaves, old_leaves) -> tuple[int, int, str] | None:
  if new_leaves == old_leaves: return
  diffs = []
  add_weak_type_hint = False
  for name, new_ty, old_ty in zip(dbg.arg_names, new_leaves, old_leaves):
    if new_ty != old_ty:
      new_str, old_str = new_ty.str_short(True), old_ty.str_short(True)
      if type(new_ty) is type(old_ty) is core.ShapedArray:
        if new_ty.sharding != old_ty.sharding:
          new_str, old_str = new_ty.str_short(True, True), old_ty.str_short(True, True)
        if new_ty.weak_type != old_ty.weak_type:
          add_weak_type_hint = True
          new_str += f'{{weak_type={new_ty.weak_type}}}'
          old_str += f'{{weak_type={old_ty.weak_type}}}'
      diffs.append(f"  * at {name}, now {new_str} and before {old_str}")
  msg = 'different input types:\n' + '\n'.join(diffs)
  if add_weak_type_hint:
    msg += 'https://docs.jax.dev/en/latest/type_promotion.html#weak-types'
  if diffs: return 3, len(diffs), msg

