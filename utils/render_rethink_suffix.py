
def render_rethink_suffix(
    illegal_template: str,
    unparsable_template: str,
    previous_response: str | None,
    previous_action: str | None,
) -> str:
    """Pick and render the right rethink suffix for the parse-failure mode.

    The two templates partition the parse-failure space:

    - ``illegal_template`` is used when the parser extracted a value but
      it wasn't a legal move (``previous_action`` is set). Must accept
      the placeholder ``{previous_action}`` -- the action string is the
      most useful signal here; we deliberately do not include the full
      previous response (it dilutes the correction signal).
    - ``unparsable_template`` is used when the parser couldn't extract
      anything (``previous_action`` is ``None``). Must accept the
      placeholder ``{previous_response}`` -- with no action string to
      show, the response itself is what the model needs to see. The
      response is truncated to the LAST 500 characters because models
      almost always put their answer at the end of the response; the
      first 500 chars usually keeps the preamble and drops the answer.

    Returns an empty string when there is no prior attempt to react to
    (``previous_response is None`` and ``previous_action`` is falsy) so
    the caller can unconditionally append the result to the prompt.
    """
    if previous_response is None and not previous_action:
        return ""
    if previous_action:
        return illegal_template.format(previous_action=previous_action)
    return unparsable_template.format(
        previous_response=(previous_response or "")[-500:],
    )

