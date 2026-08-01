
def _wrap_litellm_with_logging() -> None:
    """Replace litellm.completion with a version that prints I/O."""
    original = litellm.completion
    call_idx = 0

    def logged_completion(*args, **kwargs):
        nonlocal call_idx
        call_idx += 1
        messages = kwargs.get("messages", [])
        prompt = messages[-1]["content"] if messages else ""
        print(f"\n----- LLM call #{call_idx}: prompt -----")
        print(prompt)
        resp = original(*args, **kwargs)
        print(f"----- LLM call #{call_idx}: response -----")
        print(resp.choices[0].message.content)
        print("-" * 40)
        return resp

    litellm.completion = logged_completion


def _wrap_litellm_with_logging() -> None:
    """Replace litellm.completion with a version that prints I/O."""
    original = litellm.completion
    call_idx = 0

    def logged_completion(*args, **kwargs):
        nonlocal call_idx
        call_idx += 1
        messages = kwargs.get("messages", [])
        prompt = messages[-1]["content"] if messages else ""
        print(f"\n----- LLM call #{call_idx}: prompt -----")
        print(prompt)
        resp = original(*args, **kwargs)
        print(f"----- LLM call #{call_idx}: response -----")
        print(resp.choices[0].message.content)
        print("-" * 40)
        return resp

    litellm.completion = logged_completion


def _wrap_litellm_with_logging() -> None:
    """Replace litellm.completion with a version that prints I/O."""
    original = litellm.completion
    call_idx = 0

    def logged_completion(*args, **kwargs):
        nonlocal call_idx
        call_idx += 1
        messages = kwargs.get("messages", [])
        prompt = messages[-1]["content"] if messages else ""
        print(f"\n----- LLM call #{call_idx}: prompt -----")
        print(prompt)
        resp = original(*args, **kwargs)
        # When streaming, returned value is an iterator -- pass through.
        if hasattr(resp, "choices"):
            print(f"----- LLM call #{call_idx}: response -----")
            print(resp.choices[0].message.content)
            print("-" * 40)
        return resp

    litellm.completion = logged_completion

