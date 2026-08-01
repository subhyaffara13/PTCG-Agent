
def dummy_dataclass(factor=1., frozen=False):
  class_ctor = FrozenDataclass if frozen else Dataclass
  return class_ctor(
      a=NestedDataclass(
          c=factor * np.ones((3,), dtype=np.float32),
          d=factor * np.ones((4,), dtype=np.float32)),
      b=factor * 2 * np.ones((5,), dtype=np.float32))

