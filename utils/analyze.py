
def analyze(
    csv_path: Path,
    baseline_name: str,
    null_name: str | None,
    n_permutations: int,
    seed: int,
) -> str:
    """Run the full analysis; return a Markdown-formatted report."""
    rows = _load(csv_path)
    if not rows:
        return "No clean rows in CSV."

    variants = sorted({r["variant"] for r in rows})
    if baseline_name not in variants:
        raise SystemExit(
            f"baseline variant '{baseline_name}' not found. "
            f"Available: {variants}"
        )
    if null_name and null_name not in variants:
        print(
            f"# warning: null variant '{null_name}' not in data; "
            f"no calibrated noise floor",
            file=sys.stderr,
        )
        null_name = None

    models = _models_in(rows)
    baseline_pairs = _variant_pairs(rows, baseline_name)
    rng = random.Random(seed)

    lines: list[str] = []
    lines.append(f"# Permutation-test analysis")
    lines.append("")
    lines.append(f"- CSV: `{csv_path}`")
    lines.append(f"- Baseline: `{baseline_name}` ({len(baseline_pairs)} complete pairs)")
    if null_name:
        null_pairs = _variant_pairs(rows, null_name)
        lines.append(f"- Null: `{null_name}` ({len(null_pairs)} complete pairs)")
    lines.append(f"- Permutations per test: {n_permutations}")
    lines.append(f"- Models ({len(models)}): {', '.join(models)}")
    lines.append("")

    # Noise floor: null vs baseline observed + its permutation distribution.
    noise_floor_observed: float | None = None
    if null_name:
        null_observed = _observed_delta(
            baseline_pairs, null_pairs, models,
        )
        null_dist = _permutation_distribution(
            baseline_pairs, null_pairs, models, n_permutations, rng,
        )
        nm, ns = _summary_stats(null_dist)
        noise_floor_observed = float(null_observed)
        lines.append(f"## Noise floor")
        lines.append("")
        lines.append(
            f"Observed Σ|Δrank| of `{null_name}` vs `{baseline_name}`: "
            f"**{null_observed}**"
        )
        lines.append("")
        lines.append(
            f"Distribution under label-permutation: mean **{nm:.2f}**, "
            f"sd **{ns:.2f}**"
        )
        lines.append("")
        lines.append(
            f"This is the Σ|Δrank| we expect from LLM-sampling noise alone, "
            f"when prompts are byte-identical. Any real variant whose "
            f"observed Σ|Δrank| sits comfortably above this is a "
            f"statistically detectable shift."
        )
        lines.append("")

    # Each real variant: observed Σ|Δrank|, permutation p-value.
    lines.append(f"## Per-variant tests vs `{baseline_name}`")
    lines.append("")
    header = (
        "| variant | n pairs | obs Σ|Δrank| | perm mean ± sd | p-value | "
        "vs noise floor |"
    )
    sep = (
        "|---------|--------:|-------------:|---------------:|--------:|"
        "----------------|"
    )
    lines.append(header)
    lines.append(sep)

    real_variants = [v for v in variants if v not in {baseline_name, null_name}]
    for v in real_variants:
        v_pairs = _variant_pairs(rows, v)
        if not v_pairs:
            lines.append(f"| {v} | 0 | — | — | — | (no pairs) |")
            continue
        observed = _observed_delta(baseline_pairs, v_pairs, models)
        dist = _permutation_distribution(
            baseline_pairs, v_pairs, models, n_permutations, rng,
        )
        m, s = _summary_stats(dist)
        p = _p_value(observed, dist)
        if noise_floor_observed is not None:
            comp = (
                "above" if observed > noise_floor_observed
                else ("at" if observed == noise_floor_observed else "below")
            )
            comp_str = f"{comp} ({observed - noise_floor_observed:+.0f})"
        else:
            comp_str = "—"
        lines.append(
            f"| {v} | {len(v_pairs)} | {observed} | "
            f"{m:.2f} ± {s:.2f} | {p:.4f} | {comp_str} |"
        )

    lines.append("")
    lines.append(
        "*p-value = fraction of label-permutations producing Σ|Δrank| ≥ "
        "observed. Small p (e.g. <0.05) means the variant reorders the "
        "leaderboard more than chance would.*"
    )
    return "\n".join(lines)


def analyze(source):
    '''Analyze the source code and return a namedtuple with the following
    fields:

        * **loc**: The number of lines of code (total)
        * **lloc**: The number of logical lines of code
        * **sloc**: The number of source lines of code (not necessarily
            corresponding to the LLOC)
        * **comments**: The number of Python comment lines
        * **multi**: The number of lines which represent multi-line strings
        * **single_comments**: The number of lines which are just comments with
            no code
        * **blank**: The number of blank lines (or whitespace-only ones)

    The equation :math:`sloc + blanks + multi + single_comments = loc` should
    always hold.  Multiline strings are not counted as comments, since, to the
    Python interpreter, they are not comments but strings.
    '''
    lloc = comments = single_comments = multi = blank = sloc = 0
    lines = (l.strip() for l in source.splitlines())
    lineno = 1
    for line in lines:
        try:
            # Get a syntactically complete set of tokens that spans a set of
            # lines
            tokens, parsed_lines = _get_all_tokens(line, lines)
        except StopIteration:
            raise SyntaxError('SyntaxError at line: {0}'.format(lineno))

        lineno += len(parsed_lines)

        comments += sum(
            1 for t in tokens if TOKEN_NUMBER(t) == tokenize.COMMENT
        )

        # Identify single line comments, conservatively
        if is_single_token(tokenize.COMMENT, tokens):
            single_comments += 1

        # Identify docstrings, conservatively
        elif is_single_token(tokenize.STRING, tokens):
            _, _, (start_row, _), (end_row, _), _ = tokens[0]
            if end_row == start_row:
                # Consider single-line docstrings separately from other
                # multiline docstrings
                single_comments += 1
            else:
                multi += sum(1 for l in parsed_lines if l)  # Skip empty lines
                blank += sum(1 for l in parsed_lines if not l)
        else:  # Everything else is either code or blank lines
            for parsed_line in parsed_lines:
                if parsed_line:
                    sloc += 1
                else:
                    blank += 1

        # Process logical lines separately
        lloc += _logical(tokens)

    loc = sloc + blank + multi + single_comments
    return Module(loc, lloc, sloc, comments, multi, blank, single_comments)


def analyze(
    exported_program: torch.export.ExportedProgram,
    registry: _registration.ONNXRegistry | None = None,
    file=None,
) -> None:
    """Analyze the compatibility of the exported program."""
    # Get basic information about the model
    model_info = ModelInfo()
    model_info.parameter_count, model_info.buffer_count = _count_weights(
        exported_program
    )
    model_info.fx_node_count = len(exported_program.graph.nodes)
    model_info.fx_node_target_count = _count_fx_targets(exported_program)
    inputs, outputs = _get_io_specs(exported_program)
    model_info.inputs = inputs
    model_info.outputs = outputs

    if registry is None:
        registry = _registration.ONNXRegistry.from_torchlib()

    # Try to find ops for every node in the graph
    for node in exported_program.graph.nodes:
        model_info.fx_node_op_count[node.op] += 1
        if node.op == "call_function":
            try:
                onnx_function, message = _dispatching.dispatch(node, registry)
            except Exception as e:
                message = "Critical Error in dispatcher:\n"
                formatted_exception = "\n".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )
                message += f"```pytb\n{formatted_exception}\n```\n"
                onnx_function = None
            if onnx_function is None:
                model_info.dispatch_failures.append((node, message))

    # Print the results
    report = _format_model_info(model_info)
    print(report, file=file, flush=True)

