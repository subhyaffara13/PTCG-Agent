
def _fake_param_sharding():
  return {
      'my/fake/module': {
          'w': FakeShardSpec(0),
          'b': FakeShardSpec(1),
      },
      'my/other/fake/module': {
          'w': FakeShardSpec(2),
          'b': FakeShardSpec(3),
      },
  }

