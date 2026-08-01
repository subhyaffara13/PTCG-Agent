
def register_memory_profiler(profiler: MemoryProfiler | None) -> None:
  global _profiler
  _profiler = profiler

