
def register_comm_lowerings():
    """
    Register lowerings for the comm subsystem.
    """
    try:
        torch.ops._c10d_functional.all_reduce
    except AttributeError:
        log.info(
            "Inductor support for distributed collectives depends on building "
            "torch.distributed"
        )
        return

    from .lowering import (
        add_layout_constraint,
        clone,
        constrain_to_fx_strides,
        copy_,
        register_lowering,
    )

    def register_comm_lowering(fn):
        add_layout_constraint(fn, constrain_to_fx_strides)
        return register_lowering(fn)

    c10d = torch.ops._c10d_functional

    @register_comm_lowering(c10d.all_reduce)  # type: ignore[misc]
    def _all_reduce(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: "torch.distributed.distributed_c10d.GroupName",
    ) -> ir.TensorBox:
        if _should_lower_as_one_shot_all_reduce(inp, reduce_op, group_name):
            return _one_shot_all_reduce(inp, reduce_op, group_name)

        # Lower as c10d.all_reduce_
        inp = clone(inp)
        if config.reorder_for_compute_comm_overlap:
            # The horizontal fusion of this clone often severely delays the
            # scheduling of the all_reduce_ node. Horizontally fusing this
            # clone can almost never out-perform scheduling the all_reduce_
            # earlier. Also in most cases, this clone is eliminated via
            # in-place reuse. Therefore, we tell the scheduler to not fuse it.
            inp.realize()
            V.graph.no_fuse_buffer_names.add(inp.get_name())
        # pyrefly: ignore [bad-assignment]
        inp = ir.ExternKernel.require_contiguous(inp)
        # Because we are lowering as inplace c10d.all_reduce_, we should generate
        # _AllReduce_Kernel instead of _AllReduceKernel.
        ir._AllReduce_Kernel.create_inplace(
            c10d.all_reduce_.default,
            inp,  # type: ignore[arg-type]
            reduce_op,
            group_name,  # type: ignore[arg-type]
        )
        return inp  # type: ignore[return-value]

    @register_comm_lowering(c10d.all_reduce_)  # type: ignore[misc]
    def _all_reduce_(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: "torch.distributed.distributed_c10d.GroupName",
    ) -> ir.TensorBox:
        if _should_lower_as_one_shot_all_reduce(inp, reduce_op, group_name):
            ret = copy_(
                inp,
                _one_shot_all_reduce(inp, reduce_op, group_name),
            )
            mark_as_skip_wait(ret)
            return inp

        # Lower as c10d.all_reduce_
        # pyrefly: ignore [bad-assignment]
        inp = ir.ExternKernel.require_contiguous(inp)
        ir._AllReduce_Kernel.create_inplace(
            c10d.all_reduce_.default,
            inp,  # type: ignore[arg-type]
            reduce_op,
            group_name,  # type: ignore[arg-type]
        )
        return inp  # type: ignore[return-value]

    @register_comm_lowering(c10d.all_reduce_coalesced)
    def _all_reduce_coalesced(inputs, reduce_op, group_name):
        inputs = [clone(inp) for inp in inputs]
        ir._CollectiveKernel.create_inplace(
            c10d.all_reduce_coalesced_.default,
            inputs,
            reduce_op,
            group_name,
        )
        return inputs

    @register_comm_lowering(c10d.all_reduce_coalesced_)
    def _all_reduce_coalesced_(inputs, reduce_op, group_name):
        ir._CollectiveKernel.create_inplace(
            c10d.all_reduce_coalesced_.default,
            inputs,
            reduce_op,
            group_name,
        )
        return inputs

    def _create_out_of_place(kernel, inputs, *args) -> ir.IRNode:
        node = ir._CollectiveKernel.create_out_of_place(kernel, inputs, *args)
        assert isinstance(node, ir.IRNode)
        return ir.TensorBox.create(node)

    @register_comm_lowering(c10d.all_gather_into_tensor)
    def _all_gather_into_tensor(inp, group_size, group_name):
        return _create_out_of_place(
            c10d.all_gather_into_tensor.default,
            inp,
            group_size,
            group_name,
        )

    @register_comm_lowering(c10d.all_gather_into_tensor_coalesced)
    def _all_gather_into_tensor_coalesced(inputs, group_size, group_name):
        return pytree.tree_map(
            ir.TensorBox.create,
            ir._CollectiveKernel.create_out_of_place(
                c10d.all_gather_into_tensor_coalesced.default,
                inputs,
                group_size,
                group_name,
            ),
        )

    @register_comm_lowering(c10d.all_gather_into_tensor_out)
    def _all_gather_into_tensor_out(inp, group_size, group_name, *, out):
        ir._CollectiveKernel.create_inplace(
            c10d.all_gather_into_tensor_out.default,
            inp,
            group_size,
            group_name,
            out=out,
        )
        return out

    @register_comm_lowering(c10d.reduce_scatter_tensor)
    def _reduce_scatter_tensor(inp, reduce_op, group_size, group_name):
        return _create_out_of_place(
            c10d.reduce_scatter_tensor.default,
            inp,
            reduce_op,
            group_size,
            group_name,
        )

    @register_comm_lowering(c10d.reduce_scatter_tensor_out)
    def _reduce_scatter_tensor_out(inp, reduce_op, group_size, group_name, *, out):
        ir._CollectiveKernel.create_inplace(
            c10d.reduce_scatter_tensor_out.default,
            inp,
            reduce_op,
            group_size,
            group_name,
            out=out,
        )
        return out

    @register_comm_lowering(c10d.reduce_scatter_tensor_coalesced)
    def _reduce_scatter_tensor_coalesced(inputs, reduce_op, group_size, group_name):
        return pytree.tree_map(
            ir.TensorBox.create,
            ir._CollectiveKernel.create_out_of_place(
                c10d.reduce_scatter_tensor_coalesced.default,
                inputs,
                reduce_op,
                group_size,
                group_name,
            ),
        )

    @register_comm_lowering(c10d.all_to_all_single)
    def _all_to_all_single(inp, output_split_sizes, input_split_sizes, group_name):
        return _create_out_of_place(
            c10d.all_to_all_single.default,
            inp,
            output_split_sizes,
            input_split_sizes,
            group_name,
        )

    @register_comm_lowering(c10d.broadcast)
    def _broadcast(inp, src, group_name):
        inp = clone(inp)
        ir._CollectiveKernel.create_inplace(
            c10d.broadcast_.default, inp, src, group_name
        )
        return inp

    @register_comm_lowering(c10d.broadcast_)
    def _broadcast_(inp, src, group_name):
        ir._CollectiveKernel.create_inplace(
            c10d.broadcast_.default, inp, src, group_name
        )
        return inp

    @register_comm_lowering(torch.ops._dtensor.shard_dim_alltoall)
    def _shard_dim_alltoall(inp, gather_dim, shard_dim, group_name):
        return _create_out_of_place(
            torch.ops._dtensor.shard_dim_alltoall.default,
            inp,
            gather_dim,
            shard_dim,
            group_name,
        )

    @register_comm_lowering(c10d.wait_tensor)
    def _wait_tensor(inp):
        if should_skip_wait(inp):
            return inp

        ir._WaitKernel.create_wait(c10d.wait_tensor.default, inp)
        return inp

    @register_comm_lowering(c10d.isend)  # type: ignore[misc]
    def _isend(inp, dst, tag, group_name):
        inp = ir.ExternKernel.require_contiguous(inp)
        return _create_out_of_place(c10d.isend.default, inp, dst, tag, group_name)

    @register_comm_lowering(c10d.irecv)  # type: ignore[misc]
    def _irecv(inp, src, tag, group_name):
        inp = ir.ExternKernel.require_contiguous(inp)
        ir._CollectiveKernel.create_inplace(
            c10d.irecv.default, inp, src, tag, group_name
        )
        return inp

    @register_comm_lowering(c10d.batch_p2p_ops)  # type: ignore[misc]
    def _batch_p2p_ops(op_list, peer_list, tag_list, tensors, group_name):
        tensors = [ir.ExternKernel.require_contiguous(t) for t in tensors]
        kernel = c10d.batch_p2p_ops.default
        with V.graph.fake_mode:
            (
                example_output,
                tensor_args,
                non_tensor_args,
                unflatten_args,
                unbacked_bindings,
            ) = ir._CollectiveKernel.process_kernel(
                kernel,
                op_list,
                peer_list,
                tag_list,
                tensors,
                group_name,
            )
        assert not unbacked_bindings, f"{kernel} {unbacked_bindings}"
        for op, tensor_arg in zip(op_list, tensor_args):
            tensor_arg.realize()
            if op == "irecv":
                V.graph.mark_buffer_mutated(tensor_arg.get_name())

        device = tensor_args[0].get_device()
        packed = ir._CollectiveKernel(
            ir.MultiOutputLayout(device=device),
            kernel,
            tensor_args,
            non_tensor_args,
            unflatten_args,
        )

        results = []
        for i, (op, t, ex_out) in enumerate(zip(op_list, tensors, example_output)):
            if op == "irecv":
                packed.mutation_outputs.append(
                    ir.MutationOutput(ir.NoneLayout(device=device), t, packed)
                )
                packed.alias_names.append(t.get_name())
                results.append(t)
            else:
                # isend: 0-element placeholder output connected to the collective
                placeholder = ir.MultiOutput(
                    ir._CollectiveKernel.tensor_to_layout(ex_out),
                    packed,
                    [(list, i)],
                )
                results.append(ir.TensorBox.create(placeholder))
        return results

