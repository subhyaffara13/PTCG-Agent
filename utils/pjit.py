from typing import Any, Callable

def pjit(
    fun: Callable,
    in_shardings: Any = UNSPECIFIED,
    out_shardings: Any = UNSPECIFIED,
    static_argnums: int | Sequence[int] | None = None,
    static_argnames: str | Iterable[str] | None = None,
    donate_argnums: int | Sequence[int] | None = None,
    donate_argnames: str | Iterable[str] | None = None,
    keep_unused: bool = False,
    device: xc.Device | None = None,
    backend: str | None = None,
    inline: bool = False,
    compiler_options: dict[str, Any] | None = None,
) -> JitWrapped:
  """`jax.experimental.pjit.pjit` has been deprecated. Please use `jax.jit`."""
  return make_jit(
      fun, in_shardings=in_shardings, out_shardings=out_shardings,
      static_argnums=static_argnums, static_argnames=static_argnames,
      donate_argnums=donate_argnums, donate_argnames=donate_argnames,
      keep_unused=keep_unused, device=device, backend=backend, inline=inline,
      compiler_options=compiler_options, use_resource_env=True)

