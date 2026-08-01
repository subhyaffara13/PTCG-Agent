
def test_dataclasses():
    # Issue #500
    @dataclasses.dataclass
    class A:
        x: int
        y: str

    @dataclasses.dataclass
    class B:
        a: A

    a = A(1, "test")
    before = B(a)
    save = dill.dumps(before)
    after = dill.loads(save)
    assert before != after # classes don't match
    assert before == B(A(**dataclasses.asdict(after.a)))
    assert dataclasses.asdict(before) == dataclasses.asdict(after)

