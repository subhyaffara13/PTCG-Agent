import json

def print_repro_on_failure(repro_parts):
    try:
        yield
    except unittest.SkipTest:
        raise
    except Exception as e:
        # Get the index of the sample input that failed the test if possible.
        sample_isolation_prefix = ""
        tracked_input = getattr(e, "_tracked_input", None)
        if tracked_input is not None:
            sample_isolation_prefix = f"PYTORCH_OPINFO_SAMPLE_INPUT_INDEX={tracked_input.index}"

        repro_str = " ".join(filter(None, (sample_isolation_prefix, *repro_parts)))

        open_source_signpost(
            subsystem="test_repros",
            name="test_failure",
            parameters=json.dumps(
                {
                    "repro": " ".join(filter(None, (sample_isolation_prefix, *repro_parts))),
                }
            ),
        )

        repro_msg = f"""
To execute this test, run the following from the base repo dir:
    {repro_str}

This message can be suppressed by setting PYTORCH_PRINT_REPRO_ON_FAILURE=0"""

        # NB: Hacking the exception args is the cleanest way I've found to append
        # failure reproduction info without poisoning the stack trace.
        if len(e.args) >= 1:
            e.args = (f"{e.args[0]}\n{repro_msg}", *e.args[1:])
        raise

