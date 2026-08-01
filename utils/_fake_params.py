
def _fake_params():
  return {
      'my/fake/module': {
          'w': jnp.zeros((1, 2)),
          'b': jnp.zeros((3, 4)),
      },
      'my/other/fake/module': {
          'w': jnp.zeros((1, 2)),
          'b': jnp.zeros((3, 4)),
      },
  }

