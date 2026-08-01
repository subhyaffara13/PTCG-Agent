
def platform_dependent(*args: Any,
                       default: Callable[..., _T] | None = None,
                       **per_platform: Callable[..., _T]):
  """Stages out platform-specific code.

  In JAX the actual platform on which a computation is run is determined
  very late, e.g., based on where the data is located. When using AOT
  lowering or serialization, the computation may be compiled and executed
  on a different machine, or even on a platform that is not available at
  lowering time. This means that it is not safe to write platform-dependent
  code using Python conditionals, e.g., based on the current default
  JAX platform. Instead, one can use ``platform_dependent``:

  Usage::

      def cpu_code(*args): ...
      def tpu_code(*args): ...
      def other_platforms_code(*args): ...
      res = platform_dependent(*args, cpu=cpu_code, tpu=tpu_code,
                               default=other_platforms_code)

  When the staged out code is executed on a CPU, this is equivalent to
  ``cpu_code(*args)``, on a TPU is equivalent to ``tpu_code(*args)`` and on
  any other platform to ``other_platforms_code(*args)``.
  Unlike a Python conditional, all alternatives are traced
  and staged out to Jaxpr. This is similar to, and is implemented in terms of,
  :func:`~switch`, from which it inherits the behavior
  under transformations.

  Unlike a :func:`~switch` the choice of what gets executed is made earlier:
  in most cases during lowering when the lowering platform is known; in the
  rare case of multi-platform lowering and serialization, the StableHLO code
  will contain a conditional on the actual platform. This conditional is
  resolved just in time prior to compilation when the compilation platform is
  known. This means that the compiler actually never sees a conditional.

  Args:
    *args: JAX arrays passed to each of the branches. May be PyTrees.
    **per_platform: branches to use for different platforms. The branches are
      JAX callables invoked with ``*args``. The keywords are platform names,
      e.g., 'cpu', 'tpu', 'cuda', 'rocm'.
    default: optional default branch to use for a platform not mentioned in
      ``per_platform``. If there is no ``default`` there will be an error when
      the code is lowered for a platform not mentioned in ``per_platform``.

  Returns:
    The value ``per_platform[execution_platform](*args)``.
  """
  # Join identical branches
  branches_platforms_list: list[tuple[list[str], Callable]] = []
  for pname, pbranch in per_platform.items():
    if not callable(pbranch):
      raise TypeError(f"lax.platform_dependent: the '{pname}' branch must "
                      "be a callable.")
    if pname == "gpu":
      raise ValueError("Use 'cuda' or 'rocm' for lax.platform_dependent.")
    for ps, b in branches_platforms_list:
      if b == pbranch:
        ps.append(pname)
        break
    else:
      branches_platforms_list.append(([pname], pbranch))

  platforms_lists, branches = util.unzip2(branches_platforms_list)
  branches_platforms: BranchesPlatforms = tuple(tuple(ps) for ps in platforms_lists)
  if default is not None:
    if not callable(default):
      raise TypeError("lax.platform_dependent: the 'default' branch must "
                      "be a callable.")
    branches = branches + (default,)
    branches_platforms = branches_platforms + (None,)
  platform_index = platform_index_p.bind(platforms=branches_platforms)

  if core.is_concrete(platform_index):
    return branches[int(platform_index)](*args)
  return _switch_internal(platform_index, branches, args,
                          branches_platforms=branches_platforms)

