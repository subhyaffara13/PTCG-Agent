import functools

def _get_opt(self: absltest.TestCase, opt_name: str):
  if opt_name == 'optimistic_adam':
    opt_ = getattr(alias, opt_name)

    @functools.wraps(opt_)
    def opt(*args, **kwargs):
      with self.assertWarnsRegex(
          DeprecationWarning, 'use `optimistic_adam_v2` instead'
      ):
        return opt_(*args, **kwargs)

    return opt

  return getattr(alias, opt_name)

