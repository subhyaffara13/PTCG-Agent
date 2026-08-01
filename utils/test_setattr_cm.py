
def test_setattr_cm():
    class A:
        cls_level = object()
        override = object()

        def __init__(self):
            self.aardvark = 'aardvark'
            self.override = 'override'
            self._p = 'p'

        def meth(self):
            ...

        @classmethod
        def classy(cls):
            ...

        @staticmethod
        def static():
            ...

        @property
        def prop(self):
            return self._p

        @prop.setter
        def prop(self, val):
            self._p = val

    class B(A):
        ...

    other = A()

    def verify_pre_post_state(obj):
        # When you access a Python method the function is bound
        # to the object at access time so you get a new instance
        # of MethodType every time.
        #
        # https://docs.python.org/3/howto/descriptor.html#functions-and-methods
        assert obj.meth is not obj.meth
        # normal attribute should give you back the same instance every time
        assert obj.aardvark is obj.aardvark
        assert a.aardvark == 'aardvark'
        # and our property happens to give the same instance every time
        assert obj.prop is obj.prop
        assert obj.cls_level is A.cls_level
        assert obj.override == 'override'
        assert not hasattr(obj, 'extra')
        assert obj.prop == 'p'
        assert obj.monkey == other.meth
        assert obj.cls_level is A.cls_level
        assert 'cls_level' not in obj.__dict__
        assert 'classy' not in obj.__dict__
        assert 'static' not in obj.__dict__

    a = B()

    a.monkey = other.meth
    verify_pre_post_state(a)
    with cbook._setattr_cm(
            a, prop='squirrel',
            aardvark='moose', meth=lambda: None,
            override='boo', extra='extra',
            monkey=lambda: None, cls_level='bob',
            classy='classy', static='static'):
        # because we have set a lambda, it is normal attribute access
        # and the same every time
        assert a.meth is a.meth
        assert a.aardvark is a.aardvark
        assert a.aardvark == 'moose'
        assert a.override == 'boo'
        assert a.extra == 'extra'
        assert a.prop == 'squirrel'
        assert a.monkey != other.meth
        assert a.cls_level == 'bob'
        assert a.classy == 'classy'
        assert a.static == 'static'

    verify_pre_post_state(a)

