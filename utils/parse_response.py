
def parse_response(
    *,
    text_format: type[TextFormatT] | Omit,
    input_tools: Iterable[ToolParam] | Omit | None,
    response: Response | ParsedResponse[object],
) -> ParsedResponse[TextFormatT]:
    output_list: List[ParsedResponseOutputItem[TextFormatT]] = []

    for output in response.output:
        if output.type == "message":
            content_list: List[ParsedContent[TextFormatT]] = []
            for item in output.content:
                if item.type != "output_text":
                    content_list.append(item)
                    continue

                content_list.append(
                    construct_type_unchecked(
                        type_=ParsedResponseOutputText[TextFormatT],
                        value={
                            **item.to_dict(),
                            "parsed": parse_text(item.text, text_format=text_format),
                        },
                    )
                )

            output_list.append(
                construct_type_unchecked(
                    type_=ParsedResponseOutputMessage[TextFormatT],
                    value={
                        **output.to_dict(),
                        "content": content_list,
                    },
                )
            )
        elif output.type == "function_call":
            output_list.append(
                construct_type_unchecked(
                    type_=ParsedResponseFunctionToolCall,
                    value={
                        **output.to_dict(),
                        "parsed_arguments": parse_function_tool_arguments(
                            input_tools=input_tools, function_call=output
                        ),
                    },
                )
            )
        elif (
            output.type == "computer_call"
            or output.type == "file_search_call"
            or output.type == "web_search_call"
            or output.type == "tool_search_call"
            or output.type == "tool_search_output"
            or output.type == "additional_tools"
            or output.type == "reasoning"
            or output.type == "compaction"
            or output.type == "mcp_call"
            or output.type == "mcp_approval_request"
            or output.type == "mcp_approval_response"
            or output.type == "image_generation_call"
            or output.type == "code_interpreter_call"
            or output.type == "local_shell_call"
            or output.type == "local_shell_call_output"
            or output.type == "shell_call"
            or output.type == "shell_call_output"
            or output.type == "apply_patch_call"
            or output.type == "apply_patch_call_output"
            or output.type == "mcp_list_tools"
            or output.type == "exec"
            or output.type == "custom_tool_call"
            or output.type == "function_call_output"
            or output.type == "computer_call_output"
            or output.type == "custom_tool_call_output"
        ):
            output_list.append(output)
        elif TYPE_CHECKING:  # type: ignore
            assert_never(output)
        else:
            output_list.append(output)

    return construct_type_unchecked(
        type_=ParsedResponse[TextFormatT],
        value={
            **response.to_dict(),
            "output": output_list,
        },
    )


def parse_response(
    response: str,
    legal_action_strings: Sequence[str] | None,
) -> ParseResult:
    """Extract a move from the LLM response.

    For Cluemaster (free-form, ``legal_action_strings is None``):
        Returns ``ParseResult(submission={"clue": ..., "number": ...})``.

    For Guesser (enumerable):
        Returns ``ParseResult(legal_action=matched_string)``.
    """
    parsed = _extract_json(response)
    if parsed is None:
        return ParseResult(raw_action=response[:200])

    # --- Cluemaster (free-form) ---
    thinking = parsed.get("thinking")
    if legal_action_strings is None:
        clue = parsed.get("clue")
        number = parsed.get("number")
        if clue is not None and number is not None:
            try:
                num = int(number)
            except (ValueError, TypeError):
                return ParseResult(raw_action=response[:200], thoughts=thinking)
            return ParseResult(
                submission={"clue": str(clue), "number": num},
                raw_action=json.dumps({"clue": str(clue), "number": num}),
                thoughts=thinking,
            )
        return ParseResult(raw_action=response[:200], thoughts=thinking)

    # --- Guesser (enumerable) ---
    guess = parsed.get("guess")
    if guess is None:
        return ParseResult(raw_action=response[:200], thoughts=thinking)

    raw = str(guess)
    try:
        guess_int = int(guess)
    except (ValueError, TypeError):
        return ParseResult(legal_action=None, raw_action=raw, thoughts=thinking)

    # Match by index prefix in legal_action_strings (e.g. "4: APPLE").
    target = f"{guess_int}:"
    for legal in legal_action_strings:
        if legal.startswith(target):
            return ParseResult(legal_action=legal, raw_action=raw, thoughts=thinking)

    return ParseResult(legal_action=None, raw_action=raw, thoughts=thinking)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_cell_to_legal)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_notation_to_legal)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str] | None,
) -> ParseResult:
    """Extract the model's chosen action and match it to a legal one.

    Single intent surface: the LAST JSON object in the response that
    carries any of the bargaining payload keys. No prose-scan fallback --
    if the model didn't write a structured answer, we return
    ``legal_action=None`` so the rethink loop asks for one.
    """
    if not legal_action_strings:
        return ParseResult(raw_action=None)

    payload = extract_last_json_object(response, required_keys=_PAYLOAD_KEYS)
    if payload is None:
        return ParseResult(legal_action=None, raw_action=None)

    candidate = _payload_to_action_string(payload)
    if candidate is None:
        # JSON parsed but didn't decode to any valid action shape (unknown
        # verb, no keep dict, non-int counts, etc.). Route to the
        # unparsable rethink rather than the illegal one, since the illegal
        # template's diagnosis ("kept counts exceed the pool, or Agree with
        # no offer") wouldn't fit a shape failure.
        return ParseResult(legal_action=None, raw_action=None)

    raw_repr = json.dumps(payload, separators=(",", ":"))
    legal_set = set(legal_action_strings)
    if candidate in legal_set:
        return ParseResult(legal_action=candidate, raw_action=raw_repr)
    return ParseResult(legal_action=None, raw_action=raw_repr)


def parse_response(response: str, legal_action_strings: Sequence[str]) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(
        response,
        legal_action_strings,
        matcher=_match_move_to_legal,
    )


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str],
) -> ParseResult:
    """Extract a legal chess move from the model response.

    Two-stage pipeline matching GameArena's approach:
    1. ``RuleBasedMoveParser`` — extract text after "Final Answer:" tag
    2. ``ChessSoftParser`` — validate/match against legal moves
    """
    # Stage 1: extract candidate move
    raw = _extract_move_from_response(response)

    if raw is None:
        return ParseResult(legal_action=None, raw_action=None)

    # Stage 2: soft-match against legal moves
    matched = _soft_match_move(raw, legal_action_strings)

    if matched is not None:
        return ParseResult(legal_action=matched, raw_action=raw)

    return ParseResult(legal_action=None, raw_action=raw)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(
        response, legal_action_strings, matcher=_match_move,
    )


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str],
) -> ParseResult:
    """Extract a legal Connect Four move from the model response.

    Multi-stage parser:
    1. Look for ``Final Answer: <column>``
    2. Scan for last digit in the response matching a legal column
    """
    # Stage 1: "Final Answer: <digit>" -- use the LAST occurrence (matching
    # GameArena's ``parse_move_from_response`` which uses ``rfind`` on the
    # action tag). Models that consider then revise their answer will
    # restate the final answer; the trailing one is the intent.
    matches = list(_FINAL_ANSWER_RE.finditer(response))
    match = matches[-1] if matches else None
    raw = match.group(1) if match else None
    if raw is not None:
        matched = _match_column_to_legal(raw, legal_action_strings)
        if matched is not None:
            return ParseResult(legal_action=matched, raw_action=raw)

    # Stage 2: scan for digits from the end of the response
    for digit_match in reversed(list(re.finditer(r"\d+", response))):
        column = digit_match.group()
        matched = _match_column_to_legal(column, legal_action_strings)
        if matched is not None:
            return ParseResult(legal_action=matched, raw_action=column)

    return ParseResult(raw_action=raw)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_move_to_legal)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_to_legal)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_move_to_legal)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_move_to_legal)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_move_to_legal)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str] | None,
) -> ParseResult:
    if not legal_action_strings:
        return ParseResult(raw_action=response[:200])

    legal_set = set(legal_action_strings)
    payload = _extract_payload(response)

    if payload is None:
        # The model didn't give a structured answer at all. Return None
        # so the rethink loop asks for one rather than guessing at the
        # intent from bracket-lists or stray "accept" keywords in the
        # prose (both of which silently substituted moves the model
        # never chose).
        return ParseResult(legal_action=None, raw_action=None)

    # The model gave a structured answer. Trust it: submit if any
    # derived candidate is legal, otherwise surface raw_action with
    # legal_action=None so the rethink loop fires.
    raw_repr = json.dumps(payload, separators=(",", ":"))
    for candidate in _candidate_action_strings(payload):
        if candidate in legal_set:
            return ParseResult(legal_action=candidate, raw_action=raw_repr)
    return ParseResult(legal_action=None, raw_action=raw_repr)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(
        response, legal_action_strings,
        json_key="bid",
        matcher=_match_bid_to_legal,
    )


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings, matcher=_match_move_to_legal)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str],
    *,
    observation: Mapping[str, Any] | None = None,
) -> ParseResult:
    """Extract a legal poker action from the model response.

    Two-stage pipeline matching upstream:
    1. ``RuleBasedMoveParser`` -- extract suffix after the last "Final Answer:".
    2. ``PokerSoftParser`` -- soft-match against legal moves, handling the
       street-total vs ACPC cross-street-total bet-sizing convention.
    """
    raw = _extract_move_from_response(response)
    if raw is None:
        return ParseResult(legal_action=None, raw_action=None)
    if observation is None:
        # Without state context we can only return what we extracted; the
        # framework will treat this as an illegal-move retry.
        return ParseResult(legal_action=None, raw_action=raw)
    state = _deserialize_state(observation)
    if state is None:
        return ParseResult(legal_action=None, raw_action=raw)
    return parse_response_with_state(response, legal_action_strings, state)


def parse_response(
    response: str, legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(response, legal_action_strings)


def parse_response(
    response: str,
    legal_action_strings: Sequence[str],
) -> ParseResult:
    """Trust the model's JSON answer; let the rethink loop fix anything else."""
    return parse_json_action(
        response,
        legal_action_strings,
        matcher=match_ultimate_tic_tac_toe,
    )

