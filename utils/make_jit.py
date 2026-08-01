
def make_jit(fun: Callable,
             *,
             in_shardings: Any,
             out_shardings: Any,
             static_argnums: int | Sequence[int] | None,
             static_argnames: str | Iterable[str] | None,
             donate_argnums: int | Sequence[int] | None,
             donate_argnames: str | Iterable[str] | None,
             keep_unused: bool,
             device: xc.Device | None,
             backend: str | None,
             inline: bool,
             compiler_options: dict[str, Any] | None,
             use_resource_env: bool) -> Any:
  """jit() and pjit() are thin wrappers around this function."""
  jit_info = _parse_jit_arguments(
        fun, in_shardings=in_shardings, out_shardings=out_shardings,
        static_argnums=static_argnums, static_argnames=static_argnames,
        donate_argnums=donate_argnums, donate_argnames=donate_argnames,
        keep_unused=keep_unused, device=device, backend=backend, inline=inline,
        compiler_options=compiler_options,
        use_resource_env=use_resource_env)
  return _cpp_pjit(fun, jit_info)

