import copy
import json
import os
import sys
from typing import Any

def verify(
    stub: MaybeMissing[nodes.Node], runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    """Entry point for comparing a stub to a runtime object.

    We use single dispatch based on the type of ``stub``.

    :param stub: The mypy node representing a part of the stub
    :param runtime: The runtime object corresponding to ``stub``

    """
    yield Error(object_path, "is an unknown mypy node", stub, runtime)


def verify(model, args, loss_fn=torch.sum, devices=None):
    """
    Verify that a JIT compiled model has the same behavior as its uncompiled version along with its backwards pass.

    If your model returns multiple outputs,
    you must also specify a `loss_fn` to produce a loss for which
    the backwards will be computed.

    This function has side-effects (e.g., it executes your model / saves and loads
    parameters), so don't expect the model to come out exactly the same as what
    you passed in.

    Args:
        model (compiled torch.nn.Module or function): the module/function to be
            verified.  The module/function definition MUST have been decorated with
            `@torch.jit.compile`.
        args (tuple or Tensor): the positional arguments to pass to the
            compiled function/module to be verified.  A non-tuple is assumed to
            be a single positional argument to be passed to the model.
        loss_fn (function, optional): the loss function to be applied to
            the output of the model, before backwards is invoked.  By default,
            we assume that a model returns a single result, and we :func:`torch.sum`
            before calling backwards; if this is inappropriate, you can pass your
            own loss function.  Note that if a model returns a tuple of results,
            these are passed as separate positional arguments to `loss_fn`.
        devices (iterable of device IDs, optional): the GPU devices which the
            compiled module will be run on.  This determines the RNG state we
            must save when running both compiled and uncompiled versions of the model.
    """
    # TODO: In principle, we track device information in our trace, so it
    # should be possible to check if our execution actually obeyed the 'devices'
    # the user provided.

    # TODO: Consider adding a utility function to torch.jit to test
    # for this case
    if not isinstance(model, torch._C.CompiledFunction):  # type: ignore[attr-defined]
        raise TypeError(
            "Cannot verify an uncompiled module.  Add @torch.jit.compile to compile it"
        )
    is_module = isinstance(model, Module)

    if not isinstance(args, tuple):
        args = (args,)

    if is_module:
        saved_state = copy.deepcopy(model.state_dict())

    def run_fwd_bwd(args, force_trace=False, assert_compiled=False):
        params = list(model.parameters()) if is_module else []
        in_vars, _ = _flatten((args, params))
        # We use a special API to reset the trace and compile it from scratch.
        compiled_fn = model
        if force_trace:
            compiled_fn.clear_cache()
        if assert_compiled:
            hits = compiled_fn.hits
        out = model(*args)
        if assert_compiled and compiled_fn.hits == hits:  # type: ignore[possibly-undefined]
            raise RuntimeError("failed to use the compiled function")
        if not isinstance(out, tuple):
            out = (out,)
        if loss_fn == torch.sum and len(out) != 1:
            raise ValueError(
                f"Model returns {len(out)} outputs, but default loss function "
                "(torch.sum) can only handle a single output"
            )
        out_vars, _ = _flatten(out)
        saved_outs = [
            v.detach().clone(memory_format=torch.preserve_format) for v in out_vars
        ]
        loss = loss_fn(*out)
        grads = torch.autograd.grad([loss], in_vars)
        # TODO: I'm not sure if the clone here is necessary but it is safer
        saved_grads = [
            v.detach().clone(memory_format=torch.preserve_format) for v in grads
        ]
        return (saved_outs, saved_grads)

    with torch.random.fork_rng(devices, _caller="torch.jit.verify"):
        uncompiled_outs, uncompiled_grads = run_fwd_bwd(args, force_trace=True)
        if not model.has_trace_for(*args):
            raise AssertionError("Model should have trace for the given args")

    if is_module:
        model.load_state_dict(saved_state)  # type: ignore[possibly-undefined]
    compiled_outs, compiled_grads = run_fwd_bwd(args, assert_compiled=True)

    _verify_equal(uncompiled_outs, compiled_outs)
    _verify_equal(uncompiled_grads, compiled_grads)


def verify(
    model: _ModelType,
    input_args: _InputArgsType,
    input_kwargs: _InputKwargsType | None = None,
    do_constant_folding: bool = True,
    dynamic_axes: Mapping[str, Mapping[int, str] | Mapping[str, Sequence[int]]]
    | None = None,
    input_names: Sequence[str] | None = None,
    output_names: Sequence[str] | None = None,
    training: _C_onnx.TrainingMode = _C_onnx.TrainingMode.EVAL,
    opset_version: int | None = None,
    keep_initializers_as_inputs: bool = True,
    verbose: bool = False,
    fixed_batch_size: bool = False,
    use_external_data: bool = False,
    additional_test_inputs: Sequence[_InputArgsType] | None = None,
    options: VerificationOptions | None = None,
) -> None:
    """Verify model export to ONNX against original PyTorch model.

    .. deprecated:: 2.7
        Consider using ``torch.onnx.export(..., dynamo=True)`` and use the returned
        ``ONNXProgram`` to test the ONNX model.

    Args:
        model: See :func:`torch.onnx.export`.
        input_args: See :func:`torch.onnx.export`.
        input_kwargs: See :func:`torch.onnx.export`.
        do_constant_folding: See :func:`torch.onnx.export`.
        dynamic_axes: See :func:`torch.onnx.export`.
        input_names: See :func:`torch.onnx.export`.
        output_names: See :func:`torch.onnx.export`.
        training: See :func:`torch.onnx.export`.
        opset_version: See :func:`torch.onnx.export`.
        keep_initializers_as_inputs: See :func:`torch.onnx.export`.
        verbose: See :func:`torch.onnx.export`.
        fixed_batch_size: Legacy argument, used only by rnn test cases.
        use_external_data: Explicitly specify whether to export the model with external data.
        additional_test_inputs: List of tuples. Each tuple is a group of
            input arguments to test. Currently only ``*args`` are supported.
        options: A VerificationOptions object that controls the verification behavior.

    Raises:
        AssertionError: if outputs from ONNX model and PyTorch model are not
            equal up to specified precision.
        ValueError: if arguments provided are invalid.
    """
    if options is None:
        options = VerificationOptions()

    if training == torch.onnx.TrainingMode.TRAINING:
        model.train()
    elif training == torch.onnx.TrainingMode.EVAL:
        model.eval()
    with torch.no_grad(), contextlib.ExitStack() as stack:
        model_f: str | io.BytesIO = io.BytesIO()
        if use_external_data:
            tmpdir_path = stack.enter_context(tempfile.TemporaryDirectory())
            model_f = os.path.join(tmpdir_path, "model.onnx")

        inputs_for_export = _prepare_input_for_export(input_args, input_kwargs)

        # TODO(#77679): remove this and treat mutating model separately.
        model_copy = _try_clone_model(model)
        utils._export(
            model,
            inputs_for_export,
            model_f,
            opset_version=opset_version,
            do_constant_folding=do_constant_folding,
            keep_initializers_as_inputs=keep_initializers_as_inputs,
            dynamic_axes=dynamic_axes,
            input_names=input_names,
            output_names=output_names,
            fixed_batch_size=fixed_batch_size,
            training=training,
            verbose=verbose,
        )

        _compare_onnx_pytorch_model(
            pt_model=model_copy,
            onnx_model_f=model_f,
            input_args=input_args,
            input_kwargs=input_kwargs,
            additional_test_inputs=additional_test_inputs,
            options=options,
        )


def verify(replay_path: str, verbose: bool = False) -> int:
    with open(replay_path) as f:
        replay = json.load(f)

    if replay.get("name") != "open_spiel_repeated_poker":
        print(
            f"WARNING: replay name is {replay.get('name')!r}, expected 'open_spiel_repeated_poker'",
            file=sys.stderr,
        )

    game = pyspiel.load_game(replay["configuration"]["openSpielGameString"])
    state = game.new_initial_state()
    preset_hands: list[list[int]] = replay["configuration"]["presetHands"]
    next_index = [0] * len(preset_hands)

    total_prompts = 0
    mismatches = 0
    moves_verified = 0

    for step_idx, step in enumerate(replay["steps"]):
        found = _find_move_for_step(step)
        if found is None:
            continue
        agent_idx, agent = found
        action = agent["action"]
        action_str: str = action["actionString"]
        generate_returns: list[str] = action["generate_returns"]

        _drain_chance_actions(state, preset_hands, next_index)

        if state.is_terminal():
            print(
                f"step {step_idx}: state is terminal but replay still has actions to play; aborting",
                file=sys.stderr,
            )
            return mismatches + 1

        if state.current_player() != agent_idx:
            print(
                f"step {step_idx} agent {agent_idx}: state.current_player()"
                f" = {state.current_player()} disagrees with replay; aborting",
                file=sys.stderr,
            )
            return mismatches + 1

        previous_response: str | None = None

        for attempt_idx, gr_entry in enumerate(generate_returns):
            total_prompts += 1
            try:
                old_prompt = _extract_old_prompt(gr_entry)
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print(
                    f"step {step_idx} agent {agent_idx} attempt {attempt_idx}: could not extract old prompt: {e}",
                    file=sys.stderr,
                )
                mismatches += 1
                continue

            new_prompt = harness.generate_prompt_from_state(state, previous_response=previous_response)

            if new_prompt == old_prompt:
                if verbose:
                    print(f"step {step_idx} agent {agent_idx} attempt {attempt_idx}: OK")
            else:
                mismatches += 1
                print(
                    f"\n=== MISMATCH at step {step_idx} agent {agent_idx} "
                    f"attempt {attempt_idx} (action={action_str!r}) ==="
                )
                print(_diff(old_prompt, new_prompt))

            previous_response = _extract_old_response(gr_entry)
            # parse_response_with_state is only needed if subsequent attempts
            # use raw_action -- the upstream RETHINK_REPEATED_POKER strategy
            # does not, so we can skip it entirely.

        try:
            action_id = _action_id_from_string(state, action_str)
        except ValueError as e:
            print(
                f"\nERROR: could not apply action {action_str!r} at step {step_idx}: {e}",
                file=sys.stderr,
            )
            return mismatches + 1
        state.apply_action(action_id)
        moves_verified += 1

    print(f"\nVerified {moves_verified} moves / {total_prompts} prompts; {mismatches} mismatch(es).")
    return mismatches


def verify(replay_path: str, verbose: bool = False) -> int:
    """Verify all prompts in the replay. Returns the number of mismatches."""
    with open(replay_path) as f:
        replay = json.load(f)

    if replay.get("name") != "open_spiel_connect_four":
        print(
            f"WARNING: replay name is {replay.get('name')!r}, "
            "expected 'open_spiel_connect_four'",
            file=sys.stderr,
        )

    # Honour non-default game params (e.g. Connect 5 with rows/columns/x_in_row).
    config_params = (
        replay.get("configuration", {}).get("openSpielGameParameters") or {}
    )
    game_params = {
        k: v for k, v in config_params.items()
        if k in {"rows", "columns", "x_in_row"}
    }
    game = pyspiel.load_game("connect_four", game_params)
    state = game.new_initial_state()

    total_prompts = 0
    mismatches = 0
    moves_verified = 0

    for step_idx, step in enumerate(replay["steps"]):
        found = _find_move_for_step(step)
        if found is None:
            continue
        agent_idx, agent = found
        action = agent["action"]
        action_str: str = action["actionString"]
        generate_returns: list[str] = action["generate_returns"]

        # Build the observation that the harness would have seen.
        observation = _build_observation(state)
        legal_actions = state.legal_actions()
        legal_action_strings = [state.action_to_string(a) for a in legal_actions]

        previous_response: str | None = None
        previous_action: str | None = None

        for attempt_idx, gr_entry in enumerate(generate_returns):
            total_prompts += 1
            try:
                old_prompt = _extract_old_prompt(gr_entry)
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print(
                    f"step {step_idx} agent {agent_idx} attempt {attempt_idx}: "
                    f"could not extract old prompt: {e}",
                    file=sys.stderr,
                )
                mismatches += 1
                continue

            new_prompt = generate_prompt(
                observation,
                [],  # move_history list is unused by the connect_four harness
                previous_response=previous_response,
                previous_action=previous_action,
            )

            if new_prompt == old_prompt:
                if verbose:
                    print(
                        f"step {step_idx} agent {agent_idx} attempt {attempt_idx}: OK"
                    )
            else:
                mismatches += 1
                print(
                    f"\n=== MISMATCH at step {step_idx} agent {agent_idx} "
                    f"attempt {attempt_idx} (action={action_str!r}) ==="
                )
                print(_diff(old_prompt, new_prompt))

            # Set up retry context: simulate what core_harness would pass next.
            old_response = _extract_old_response(gr_entry)
            parse_result = parse_response(old_response, legal_action_strings)
            previous_response = old_response
            previous_action = parse_result.raw_action

        # Apply the final action and advance state. Connect Four action
        # strings are "<player><column>" (e.g. "x3"), so strip the leading
        # player char to recover the column index.
        try:
            column = int(action_str[1:])
            state.apply_action(column)
        except Exception as e:
            print(
                f"\nERROR: could not apply action {action_str!r} at step {step_idx}: {e}",
                file=sys.stderr,
            )
            print("Aborting state replay; further prompts may be wrong.", file=sys.stderr)
            return mismatches + 1
        moves_verified += 1

    print(
        f"\nVerified {moves_verified} moves / {total_prompts} prompts; "
        f"{mismatches} mismatch(es)."
    )
    return mismatches


def verify(replay_path: str, verbose: bool = False) -> int:
    """Verify all prompts in the replay. Returns the number of mismatches."""
    with open(replay_path) as f:
        replay = json.load(f)

    if replay.get("name") != "open_spiel_chess":
        print(
            f"WARNING: replay name is {replay.get('name')!r}, expected 'open_spiel_chess'",
            file=sys.stderr,
        )

    game = pyspiel.load_game("chess")
    state = game.new_initial_state()

    total_prompts = 0
    mismatches = 0
    moves_verified = 0

    for step_idx, step in enumerate(replay["steps"]):
        found = _find_move_for_step(step)
        if found is None:
            continue
        agent_idx, agent = found
        action = agent["action"]
        action_str: str = action["actionString"]
        generate_returns: list[str] = action["generate_returns"]

        # Build the observation that the harness would have seen.
        observation = _build_observation(state)
        legal_actions = state.legal_actions()
        legal_action_strings = [
            state.action_to_string(state.current_player(), a) for a in legal_actions
        ]

        previous_response: str | None = None
        previous_action: str | None = None

        for attempt_idx, gr_entry in enumerate(generate_returns):
            total_prompts += 1
            try:
                old_prompt = _extract_old_prompt(gr_entry)
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print(
                    f"step {step_idx} agent {agent_idx} attempt {attempt_idx}: "
                    f"could not extract old prompt: {e}",
                    file=sys.stderr,
                )
                mismatches += 1
                continue

            new_prompt = generate_prompt(
                observation,
                [],  # move_history list is unused by the chess harness
                previous_response=previous_response,
                previous_action=previous_action,
            )

            if new_prompt == old_prompt:
                if verbose:
                    print(
                        f"step {step_idx} agent {agent_idx} attempt {attempt_idx}: OK"
                    )
            else:
                mismatches += 1
                print(
                    f"\n=== MISMATCH at step {step_idx} agent {agent_idx} "
                    f"attempt {attempt_idx} (action={action_str!r}) ==="
                )
                print(_diff(old_prompt, new_prompt))

            # Set up retry context: simulate what core_harness would pass next.
            old_response = _extract_old_response(gr_entry)
            parse_result = parse_response(old_response, legal_action_strings)
            previous_response = old_response
            previous_action = parse_result.raw_action

        # Apply the final action and advance state.
        try:
            applied = state.string_to_action(action_str)
        except Exception as e:
            print(
                f"\nERROR: could not apply action {action_str!r} at step {step_idx}: {e}",
                file=sys.stderr,
            )
            print("Aborting state replay; further prompts may be wrong.", file=sys.stderr)
            return mismatches + 1
        state.apply_action(applied)
        moves_verified += 1

    print(
        f"\nVerified {moves_verified} moves / {total_prompts} prompts; "
        f"{mismatches} mismatch(es)."
    )
    return mismatches


def verify(
    repo_id: RepoIdArg,
    repo_type: RepoTypeOpt = RepoTypeOpt.model,
    revision: RevisionOpt = None,
    cache_dir: Annotated[
        str | None,
        typer.Option(
            help="Cache directory to use when verifying files from cache (defaults to Hugging Face cache).",
        ),
    ] = None,
    local_dir: Annotated[
        str | None,
        typer.Option(
            help="If set, verify files under this directory instead of the cache.",
        ),
    ] = None,
    fail_on_missing_files: Annotated[
        bool,
        typer.Option(
            "--fail-on-missing-files",
            help="Fail if some files exist on the remote but are missing locally.",
        ),
    ] = False,
    fail_on_extra_files: Annotated[
        bool,
        typer.Option(
            "--fail-on-extra-files",
            help="Fail if some files exist locally but are not present on the remote revision.",
        ),
    ] = False,
    token: TokenOpt = None,
) -> None:
    """Verify checksums for a single repo revision from cache or a local directory.

    Examples:
      - Verify main revision in cache: `hf cache verify gpt2`
      - Verify specific revision: `hf cache verify gpt2 --revision refs/pr/1`
      - Verify dataset: `hf cache verify karpathy/fineweb-edu-100b-shuffle --repo-type dataset`
      - Verify local dir: `hf cache verify deepseek-ai/DeepSeek-OCR --local-dir /path/to/repo`
    """

    if local_dir is not None and cache_dir is not None:
        out.error("Cannot pass both --local-dir and --cache-dir. Use one or the other.")
        raise typer.Exit(code=2)

    api = get_hf_api(token=token)

    result = api.verify_repo_checksums(
        repo_id=repo_id,
        repo_type=repo_type.value if hasattr(repo_type, "value") else str(repo_type),
        revision=revision,
        local_dir=local_dir,
        cache_dir=cache_dir,
        token=token,
    )

    exit_code = 0

    if result.mismatches:
        details = "\n".join(
            f"  - {m['path']}: expected {m['expected']} ({m['algorithm']}), got {m['actual']}"
            for m in result.mismatches
        )
        out.text(f"❌ Checksum verification failed for the following file(s):\n{details}")
        exit_code = 1

    if result.missing_paths:
        if fail_on_missing_files:
            details = "\n".join(f"  - {p}" for p in result.missing_paths)
            out.text(f"❌ Missing files (present remotely, absent locally):\n{details}")
            exit_code = 1
        else:
            out.warning(
                f"{len(result.missing_paths)} remote file(s) are missing locally. "
                "Use --fail-on-missing-files for details."
            )

    if result.extra_paths:
        if fail_on_extra_files:
            details = "\n".join(f"  - {p}" for p in result.extra_paths)
            out.text(f"❌ Extra files (present locally, absent remotely):\n{details}")
            exit_code = 1
        else:
            out.warning(
                f"{len(result.extra_paths)} local file(s) do not exist on the remote repo. "
                "Use --fail-on-extra-files for details."
            )

    verified_location = result.verified_path

    if exit_code != 0:
        out.error(
            f"Verification failed for '{repo_id}' ({repo_type.value}) in {verified_location}.\n  Revision: {result.revision}"
        )
        raise typer.Exit(code=exit_code)

    out.result(
        f"Verified {result.checked_count} file(s) for {repo_type.value} '{repo_id}'. All checksums match.",
        repo_id=repo_id,
        repo_type=repo_type.value,
        checked=result.checked_count,
        path=str(verified_location),
    )

