import functools
import math


def _interpret_jaxpr(
    jaxpr,
    *args,
    ctx: InterpretContext,
    token: Array,
):
  sentinel_for_floating_point_values = (
      _SENTINEL if ctx.interpret_params.skip_floating_point_ops else None
  )
  env = interpret_utils.JaxprEnv(
      vars=jaxpr.constvars + jaxpr.invars,
      values=args,
      sentinel_for_floating_point_values=sentinel_for_floating_point_values,
  )

  # TODO(jburnim): Clean up and finish this evaluation loop.  For example:
  #  - Replace the big if-statement with a dictionary of rules.
  #  - Handle other higher-order primitives?
  _interpret = functools.partial(_interpret_jaxpr, ctx=ctx)

  for eqn in jaxpr.eqns:
    with source_info_util.user_context(
         eqn.source_info.traceback, name_stack=eqn.source_info.name_stack):
      prim = eqn.primitive
      # We defer reading the values for `eqn.invars` into each of the branches
      # of the if-elif-else statement below. This is because the else branch may
      # not need to do any reads if `interpret_params.skip_floating_point_ops`
      # is True. If this is the case, we want to avoid materializing the read
      # array into the jaxpr when this function is traced.
      deferred_invals = functools.partial(env.read_many, eqn.invars)

      if (impl := _interpret_impls.get(prim, None)):
        invals = deferred_invals()
        # TODO(jburnim): Set up a proper kernel tracing environment for `impl`.
        impl_jaxpr = jax.make_jaxpr(functools.partial(impl, **eqn.params))(
            *invals)
        token, out = _interpret_jaxpr(
            impl_jaxpr.jaxpr, *impl_jaxpr.consts, *invals, ctx=ctx, token=token
        )
        if not prim.multiple_results:
          out = out[0]

      elif prim is primitives.load_p:
        (ref, transforms, mask, _) = jax.tree.unflatten(
            eqn.params['args_tree'], deferred_invals())
        if mask is not None:
          raise NotImplementedError('masked load_p')
        memory_space = _get_memory_space_and_raise_if_hbm(
            eqn.invars[0].aval, 'load_p'
        )
        token, out = callback.io_callback(
            functools.partial(get, source_info=eqn.source_info),
            (TOKEN_SHAPE_DTYPE, eqn.outvars[0].aval),
            token,
            ctx.device_id,
            ctx.local_core_id,
            TPU_MEMORY_SPACE_IDXS[memory_space],
            ref,
            transforms,
        )

      elif prim is primitives.swap_p:
        (ref, transforms, val, mask) = jax.tree.unflatten(
            eqn.params['args_tree'], deferred_invals())
        memory_space = _get_memory_space_and_raise_if_hbm(
            eqn.invars[0].aval, 'swap_p'
        )
        token, out = callback.io_callback(
            functools.partial(swap, source_info=eqn.source_info),
            (TOKEN_SHAPE_DTYPE, eqn.outvars[0].aval),
            token,
            ctx.device_id,
            ctx.local_core_id,
            TPU_MEMORY_SPACE_IDXS[memory_space],
            ref,
            transforms,
            val,
            mask,
        )

      elif prim is primitives.delay_p:
        # TODO(jburnim): Implement this properly?
        out = []

      elif prim is mosaic_primitives.prng_seed_p:
        # TODO(jburnim): Implement this properly?
        out = []

      elif prim is mosaic_primitives.prng_random_bits_p:
        # TODO(jburnim): Implement this properly?
        out = jnp.zeros(eqn.params['shape'], jnp.int32)

      elif ((prim is lax.axis_index_p) and (ctx.mesh is not None)
            and (eqn.params['axis_name'] in ctx.mesh.shape)):
        # We are interpreting a core_map, and this lax.axis_index call is
        # querying our index along the core axis, so return our core ID.
        out = ctx.local_core_id

      elif ((prim is lax.axis_index_p)
            and (eqn.params['axis_name'] in ctx.axis_indices)):
        # We replace lax.axis_index calls in the kernel body, so that the
        # kernel body jaxpr can be run on other threads (via an io_callback)
        # without having to recreate the axis environment in those threads.
        out = ctx.axis_indices[eqn.params['axis_name']]

      elif ((prim is lax.axis_index_p) and
            (eqn.params['axis_name'] in (ctx.grid_mapping.grid_names or ()))):
        assert ctx.grid_mapping.grid_names is not None
        assert ctx.grid_point is not None
        out = ctx.grid_point[
            ctx.grid_mapping.grid_names.index(eqn.params['axis_name'])]

      elif prim is lax.cond_p:
        def _make_branch(jaxpr):
          return lambda token, *args: _interpret(jaxpr, *args, token=token)
        invals = deferred_invals()
        token, out = lax.switch(
            invals[0],
            [_make_branch(branch_jaxpr.jaxpr)
             for branch_jaxpr in eqn.params['branches']],
            token, *invals[1:])

      elif prim is lax.scan_p:
        consts, init_carry, xs = split_list(
            deferred_invals(),
            [eqn.params['num_consts'], eqn.params['num_carry']],
        )
        def _scan_body(c, a):
          token, c = c
          token, ret = _interpret(
              eqn.params['jaxpr'].jaxpr, *consts, *c, *a, token=token)
          c, b = split_list(ret, [eqn.params['num_carry']])
          return (token, c), b
        (token, carry), out = lax.scan(
            _scan_body, (token, init_carry), xs=xs,
            length=eqn.params.get('length', None))
        out = carry + out

      elif prim is lax.while_p:
        cond_consts, body_consts, init_val = split_list(
            deferred_invals(),
            [eqn.params['cond_nconsts'], eqn.params['body_nconsts']],
        )
        token, first_cond = _interpret(eqn.params['cond_jaxpr'].jaxpr,
                                       *cond_consts, *init_val, token=token)
        def _body(val):
          token, val, _ = val
          token, val = _interpret(
              eqn.params['body_jaxpr'].jaxpr, *body_consts, *val, token=token)
          token, cond = _interpret(
              eqn.params['cond_jaxpr'].jaxpr, *cond_consts, *val, token=token)
          return token, val, cond[0]
        token, out, _ = lax.while_loop(
            lambda args: args[2], _body, (token, init_val, first_cond[0]))

      elif prim is pjit.jit_p:
        invals = deferred_invals()
        token, out = _interpret(eqn.params['jaxpr'].jaxpr,
                                *eqn.params['jaxpr'].consts,
                                *invals, token=token)

      elif prim is primitives.run_scoped_p:
        if eqn.params['collective_axes']:
          raise NotImplementedError(
              'run_scoped_p with collective axes is not supported'
          )
        # Allocate a buffer or semaphore for each element of
        # eqn.params['jaxpr'].invars. It is assumed that each core
        # runs the same sequence of `run_scoped`s.
        allocs = []
        for v in eqn.params['jaxpr'].invars:
          if v.aval.memory_space is _SEMAPHORE:
            token, alloc = callback.io_callback(
                _allocate_semaphores,
                (TOKEN_SHAPE_DTYPE,
                 jax.ShapeDtypeStruct(v.aval.shape, jnp.int16)),
                token,
                ctx.device_id,
                ctx.local_core_id,
                v.aval.shape,
            )
            allocs.append(alloc)
          else:
            if not ctx.interpret_params.allow_hbm_allocation_in_run_scoped:
              memory_space = _get_memory_space_and_raise_if_hbm(
                v.aval, 'run_scoped_p', "Cannot allocate HBM in `run_scoped`."
              )
            else:
              memory_space = _forward_any_to_hbm(v.aval.memory_space)
            token, alloc = callback.io_callback(
                functools.partial(
                    _allocate_buffer, source_info=eqn.source_info
                ),
                (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct((), jnp.int16)),
                token,
                ctx.device_id,
                ctx.local_core_id,
                TPU_MEMORY_SPACE_IDXS[memory_space],
                interpret_utils.get_uninitialized_array(
                    v.aval.shape,
                    v.aval.dtype,
                    ctx.interpret_params.uninitialized_memory,
                ),
            )
            allocs.append(alloc)

        token, out = _interpret(
            eqn.params['jaxpr'], *deferred_invals(), *allocs, token=token
        )

        for a, v in zip(allocs, eqn.params['jaxpr'].invars):
          if v.aval.memory_space is _SEMAPHORE:
            # TODO(jburnim): De-allocate semaphores.
            # callback.io_callback(
            #     _deallocate_semaphores,
            #     None,
            #     device_id,
            #     a)
            pass
          else:
            token = callback.io_callback(
                functools.partial(
                    _deallocate_buffer, source_info=eqn.source_info
                ),
                TOKEN_SHAPE_DTYPE,
                token,
                ctx.device_id,
                ctx.local_core_id,
                # An exception would have been raised before `_allocate_buffer`
                # above if `memory_space` were HBM (i.e. either `pltpu.HBM` or
                # `pl.ANY`) and if this was disallowed by `interpret_params`.
                TPU_MEMORY_SPACE_IDXS[_forward_any_to_hbm(v.aval.memory_space)],
                a,
            )

      elif prim is state_primitives.get_p:
        memory_space = _get_memory_space_and_raise_if_hbm(
            eqn.invars[0].aval, 'get_p'
        )
        invals = deferred_invals()
        token, out = callback.io_callback(
            functools.partial(get, source_info=eqn.source_info),
            (TOKEN_SHAPE_DTYPE, eqn.outvars[0].aval),
            token,
            ctx.device_id,
            ctx.local_core_id,
            TPU_MEMORY_SPACE_IDXS[memory_space],
            invals[0],
            jax.tree.unflatten(eqn.params['tree'], invals[1:]),
        )

      elif prim is state_primitives.swap_p:
        memory_space = _get_memory_space_and_raise_if_hbm(
            eqn.invars[0].aval, 'swap_p'
        )
        invals = deferred_invals()
        token, out = callback.io_callback(
            functools.partial(swap, source_info=eqn.source_info),
            (TOKEN_SHAPE_DTYPE, eqn.outvars[0].aval),
            token,
            ctx.device_id,
            ctx.local_core_id,
            TPU_MEMORY_SPACE_IDXS[memory_space],
            invals[0],
            jax.tree.unflatten(eqn.params['tree'], invals[2:]),
            invals[1],
            None,
        )

      elif prim is mosaic_primitives.dma_start_p:
        src, dst, dst_sem, src_sem, target_device_id = jax.tree.unflatten(
            eqn.params['tree'], deferred_invals()
        )
        src, src_transforms = mosaic_primitives._get_ref_and_transforms(src)
        dst, dst_transforms = mosaic_primitives._get_ref_and_transforms(dst)
        dst_sem, dst_sem_transforms = mosaic_primitives._get_ref_and_transforms(
            dst_sem
        )
        src_sem, src_sem_transforms = mosaic_primitives._get_ref_and_transforms(
            src_sem
        )
        target_device_id = interpret_utils._device_id_to_logical(
            target_device_id, eqn.params['device_id_type'], ctx.axis_sizes,
            ctx.axis_indices)
        orig_src_ref, orig_dst_ref, *_ = jax.tree.unflatten(
            eqn.params['tree'], eqn.invars
        )
        src_memory_space = _forward_any_to_hbm(
            getattr(orig_src_ref.aval, 'memory_space', None)
        )
        if src_memory_space is None:
          # This is brittle. There are examples where a ref with memory_space
          # set to `None` appears as one of the `constvars` of a `run_scoped`,
          # and the corresponding input to the `run_scoped` is a buffer in VMEM
          # (and not in HBM).
          #
          # Note that pairing the buffer id, i.e. `src`, here with an incorrect
          # memory space will result in a (very visible) `KeyError` for now.
          # (This is because the buffer id alone suffices to uniquely identify
          # the buffer held by the `SharedMemory` object. The memory space can
          # be considered merely additional information (useful for debugging)
          # that is added to the key that the `SharedMemory` object uses
          # internally to look up a buffer.)
          #
          # TODO(nrink): It would be more robust if the buffer id, i.e. `src`,
          # did already encode enough information to identify the correct
          # buffer, without the need to explicitly pass the memory space to the
          # `dma_start` callback below.
          src_memory_space = mosaic_core.MemorySpace.HBM
        dst_memory_space = _forward_any_to_hbm(
            getattr(orig_dst_ref.aval, 'memory_space', None)
        )
        if dst_memory_space is None:
          # TODO(nrink): See comment for `src_memory_space` above.
          dst_memory_space = mosaic_core.MemorySpace.HBM
        token = callback.io_callback(
            functools.partial(dma_start, source_info=eqn.source_info),
            TOKEN_SHAPE_DTYPE,
            token,
            ctx.device_id,
            ctx.local_core_id,
            TPU_MEMORY_SPACE_IDXS[src_memory_space],
            src,
            src_transforms,
            TPU_MEMORY_SPACE_IDXS[dst_memory_space],
            dst,
            dst_transforms,
            state_discharge.transform_array(dst_sem, dst_sem_transforms),
            state_discharge.transform_array(src_sem, src_sem_transforms),
            target_device_id,
        )
        out = []

      elif prim is mosaic_primitives.dma_wait_p:
        src, _, dst_sem, _, _ = jax.tree.unflatten(
            eqn.params['tree'], deferred_invals()
        )
        _, src_transforms = mosaic_primitives._get_ref_and_transforms(src)
        dst_sem, dst_sem_transforms = mosaic_primitives._get_ref_and_transforms(
            dst_sem
        )
        src_ref_aval = state.transform_type(src_transforms, eqn.invars[0].aval)
        assert isinstance(src_ref_aval, state.AbstractRef)
        read_shape = src_ref_aval.shape
        read_dtype = src_ref_aval.dtype
        token = callback.io_callback(
            functools.partial(dma_wait, source_info=eqn.source_info),
            TOKEN_SHAPE_DTYPE,
            token,
            ctx.device_id,
            ctx.local_core_id,
            state_discharge.transform_array(dst_sem, dst_sem_transforms),
            math.prod(read_shape) * read_dtype.itemsize,
        )
        out = []

      elif prim is mosaic_primitives.get_barrier_semaphore_p:
        token, out = callback.io_callback(
            get_barrier_semaphore,
            (TOKEN_SHAPE_DTYPE, jax.ShapeDtypeStruct((), jnp.int16)),
            token,
            ctx.device_id,
            ctx.mosaic_params.collective_id,
        )

      elif prim is primitives.semaphore_signal_p:
        sem, sem_transforms, inc, target_device_id, core_index = (
            jax.tree.unflatten(eqn.params['args_tree'], deferred_invals()))
        target_device_id = interpret_utils._device_id_to_logical(
            target_device_id, eqn.params['device_id_type'], ctx.axis_sizes,
            ctx.axis_indices)
        token = callback.io_callback(
            functools.partial(semaphore_signal, source_info=eqn.source_info),
            TOKEN_SHAPE_DTYPE,
            token,
            ctx.device_id,
            ctx.local_core_id,
            state_discharge.transform_array(sem, sem_transforms),
            inc,
            target_device_id,
            core_index,
        )
        out = []

      elif prim is primitives.semaphore_wait_p:
        sem, sem_transforms, value, decrement = (
            jax.tree.unflatten(eqn.params['args_tree'], deferred_invals()))
        if not decrement:
          raise NotImplementedError('Non-decrementing wait is not supported.')
        token = callback.io_callback(
            semaphore_wait,
            TOKEN_SHAPE_DTYPE,
            token,
            ctx.device_id,
            ctx.local_core_id,
            state_discharge.transform_array(sem, sem_transforms),
            value,
        )
        out = []

      else:
        if ctx.interpret_params.skip_floating_point_ops and all(
            interpret_utils.is_float(ovar.aval.dtype) for ovar in eqn.outvars
        ):
          # Skip `prim.bind` since `prim` only produces floating-point values.
          # It is safe to populate `out` with avals since mapping `write` over
          #  `out` below only relies on the shape and dtype (for writing
          # `Placeholder`s).
          out = [ovar.aval for ovar in eqn.outvars]
          if not prim.multiple_results:
            out = out[0]
        else:
          bind_params = eqn.primitive.get_bind_params(eqn.params)
          out = prim.bind(*deferred_invals(), **bind_params)

      out = out if prim.multiple_results else [out]
      env.write_many(eqn.outvars, out)

  return token, env.read_many(jaxpr.outvars)

