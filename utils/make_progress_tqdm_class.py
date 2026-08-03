from typing import Callable

def make_progress_tqdm_class(callback: Callable, model_id: str) -> type:
    """Create a tqdm subclass that routes progress to a callback.

    Bars with ``unit="B"`` are download bars — aggregated via ``DownloadAggregator``.
    Other bars (e.g. "Loading weights") emit ``weights`` stage events.

    Args:
        callback (`callable`): Called with a dict payload
            ``{"status": "loading", "model": ..., "stage": ..., "progress": ...}``.
        model_id (`str`): The model ID (included in progress payloads).

    Returns:
        A tqdm subclass that forwards progress to *callback*.
    """
    from tqdm.auto import tqdm as base_tqdm

    download_aggregator = DownloadAggregator(callback, model_id)

    class ProgressTqdm(base_tqdm):  # type: ignore[misc]
        def __init__(self, *args, **kwargs):
            self.sse_unit = kwargs.get("unit") or "it"
            kwargs["disable"] = True
            super().__init__(*args, **kwargs)
            self.n = 0
            self.last_emitted = -1
            if self.sse_unit == "B":
                self._bar_id = id(self)
                download_aggregator.register(self._bar_id, self.total)

        def update(self, n=1):
            if n is None:
                n = 1
            self.n += n
            if self.sse_unit == "B":
                download_aggregator.update(self._bar_id, self.n, self.total)
            elif self.n != self.last_emitted:
                self.last_emitted = self.n
                callback(
                    {
                        "status": "loading",
                        "model": model_id,
                        "stage": "weights",
                        "progress": {"current": self.n, "total": self.total},
                    }
                )

        def __iter__(self):
            for item in self.iterable:
                self.n += 1
                if self.sse_unit == "B":
                    download_aggregator.update(self._bar_id, self.n, self.total)
                elif self.n != self.last_emitted:
                    self.last_emitted = self.n
                    callback(
                        {
                            "status": "loading",
                            "model": model_id,
                            "stage": "weights",
                            "progress": {"current": self.n, "total": self.total},
                        }
                    )
                yield item

        def close(self):
            if self.sse_unit == "B":
                download_aggregator.close(self._bar_id)
            super().close()

    return ProgressTqdm

