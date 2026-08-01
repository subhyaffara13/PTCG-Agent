
def _create_progress_bar(*, cls: type[old_tqdm], log_level: int, name: str | None = None, **kwargs) -> old_tqdm:
    """Create a progress bar.

    For our `tqdm` subclass (or subclasses of it): respects all disable signals
    (`HF_HUB_DISABLE_PROGRESS_BARS`, `disable_progress_bars()`, log level) and uses
    `disable=None` for TTY auto-detection (see https://github.com/huggingface/huggingface_hub/pull/2000),
    unless `TQDM_POSITION=-1` forces bars on (https://github.com/huggingface/huggingface_hub/pull/2698).

    For other classes: does not inject `disable` or `name`. the custom class is fully
    responsible for its own behavior. Vanilla tqdm defaults to `disable=False` (bar shows).
    Omits `name` which vanilla tqdm rejects with `TqdmKeyError`. See https://github.com/huggingface/huggingface_hub/issues/4050.
    """
    # issubclass() crashes on non-class callables (e.g. functools.partial), guard with isinstance.
    if not (isinstance(cls, type) and issubclass(cls, tqdm)):
        return cls(**kwargs)  # type: ignore[return-value]

    # HF subclass: keep the historical log-level / TTY behavior. Group-based
    # disabling is already handled in `tqdm.__init__`.
    disable = is_tqdm_disabled(log_level)
    return cls(disable=disable, name=name, **kwargs)  # type: ignore[return-value]

