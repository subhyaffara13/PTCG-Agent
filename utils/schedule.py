from typing import Callable

def schedule(
    *,
    wait: int,
    warmup: int,
    active: int,
    repeat: int = 0,
    skip_first: int = 0,
    skip_first_wait: int = 0,
) -> Callable:
    """
    Returns a callable that can be used as profiler ``schedule`` argument. The profiler will skip
    the first ``skip_first`` steps, then wait for ``wait`` steps, then do the warmup for the next ``warmup`` steps,
    then do the active recording for the next ``active`` steps and then repeat the cycle starting with ``wait`` steps.
    The optional number of cycles is specified with the ``repeat`` parameter, the zero value means that
    the cycles will continue until the profiling is finished.

    The ``skip_first_wait`` parameter controls whether the first ``wait`` stage should be skipped.
    This can be useful if a user wants to wait longer than ``skip_first`` between cycles, but not
    for the first profile. For example, if ``skip_first`` is 10 and ``wait`` is 20, the first cycle will
    wait 10 + 20 = 30 steps before warmup if ``skip_first_wait`` is zero, but will wait only 10
    steps if ``skip_first_wait`` is non-zero. All subsequent cycles will then wait 20 steps between the
    last active and warmup.
    """

    def schedule_fn(step: int) -> ProfilerAction:
        if step < 0:
            raise AssertionError(f"Step must be non-negative. Got {step}.")
        if step < skip_first:
            return ProfilerAction.NONE
        else:
            step -= skip_first
        # If wait >> skip_first and we want to grab profiling early, shift left by wait if skip_first_wait is True
        if skip_first_wait != 0:
            step += wait
        num_steps = wait + warmup + active
        if repeat > 0 and step / num_steps >= repeat:
            return ProfilerAction.NONE
        mod_step = step % num_steps
        if mod_step < wait:
            return ProfilerAction.NONE
        elif mod_step < wait + warmup:
            return ProfilerAction.WARMUP
        else:
            return (
                ProfilerAction.RECORD
                if mod_step < num_steps - 1
                else ProfilerAction.RECORD_AND_SAVE
            )

    if wait < 0 or warmup < 0 or active <= 0 or repeat < 0 or skip_first < 0:
        raise AssertionError(
            f"Invalid profiler schedule arguments. Got wait={wait} (need >= 0), warmup={warmup} (need >= 0), "
            f"active={active} (need > 0), repeat={repeat} (need >= 0), skip_first={skip_first} (need >= 0)."
        )
    if warmup == 0:
        warn(
            "Profiler won't be using warmup, this can skew profiler results",
            stacklevel=2,
        )
    return schedule_fn


def schedule(scheduler: torch._inductor.scheduler.Scheduler) -> None:
    """
    Finish the distributed autotuning by propagating the autotuning results
    between the ranks and then replacing the placeholder with the real Buffer.
    """
    assert config.distributed_max_autotune_gemm
    autotune_results = _autotune_local_nodes(scheduler)
    choices_by_index = _sync(autotune_results)
    _autotune_remote_nodes(scheduler, choices_by_index)


def schedule(ops):
  """Adds control dependencies to schedule the ops in the provided order.

  For example, schedule([a, b, c]) adds control dependencies a->b and b->c.
  """
  for src, dst in zip(ops[:-1], ops[1:]):
    control_dep(src, dst)

