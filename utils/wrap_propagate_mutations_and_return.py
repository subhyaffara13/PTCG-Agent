
def wrap_propagate_mutations_and_return(
    f: NativeFunction, functional_op: NativeFunction, inner_return_var: str
) -> str:
    mutable_arg_names = f.func.arguments.mutable_arg_names()
    (
        aliased_outer_rets,
        non_aliased_outer_rets,
    ) = get_mutable_redispatch_return_names(f, inner_return_var)
    _, non_aliased_inner_rets = get_mutable_redispatch_return_names(
        functional_op, inner_return_var
    )
    # The outer function may have a mix of aliased and non-aliased outputs,
    # But the inner functional op that we're transforming to should only have non-aliased outputs
    if len(mutable_arg_names) + len(non_aliased_outer_rets) != len(
        non_aliased_inner_rets
    ):
        raise AssertionError(
            f"Expected {len(mutable_arg_names)} + {len(non_aliased_outer_rets)} == {len(non_aliased_inner_rets)}"
        )

    # First, take all of the newly created outputs from the inner call and wrap them into functional tensors
    updates = []
    non_aliased_wrapped_ret_names = []
    for i, inner_ret in enumerate(
        non_aliased_inner_rets[: len(non_aliased_outer_rets)]
    ):
        ret_name = f"output_{i}"
        updates.append(
            f"""\
  auto output_{i} = at::functionalization::impl::to_functional_tensor({inner_ret});"""
        )
        non_aliased_wrapped_ret_names.append(ret_name)

    # Next, take all of the mutated outputs from the inner call corresponding to mutated inputs,
    # and propagate the mutations
    for outer_arg, inner_ret in zip(
        mutable_arg_names, non_aliased_inner_rets[len(non_aliased_outer_rets) :]
    ):
        updates.append(
            f"""\
  auto {outer_arg}_inner = at::functionalization::impl::from_functional_tensor({outer_arg});
  at::functionalization::impl::replace_({outer_arg}, {inner_ret});
  at::functionalization::impl::commit_update({outer_arg});
  at::functionalization::impl::sync({outer_arg});
  auto {outer_arg}_inner_updated = at::functionalization::impl::from_functional_tensor({outer_arg});
  at::functionalization::impl::propagate_xla_data_direct({outer_arg}_inner, {outer_arg}_inner_updated);"""
        )

    # Finally, we return:
    # - Any mutable arguments that also returns
    # - Any immutable returns that were created wrapping the output from the inner call
    returns_str = return_str(
        f.func.returns, aliased_outer_rets + non_aliased_wrapped_ret_names
    )
    updates_str = "\n".join(updates)
    return f"""\
{updates_str}
    {returns_str}"""

