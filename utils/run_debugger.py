from typing import Any

def run_debugger(frames: list[DebuggerFrame], thread_id: int | None,
                 **kwargs: Any):
  CliDebugger(frames, thread_id, **kwargs).run()


def run_debugger(frames: list[debugger_core.DebuggerFrame],
                 thread_id: int | None, **kwargs: Any):
  WebDebugger(frames, thread_id, **kwargs).run()

