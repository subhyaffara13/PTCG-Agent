
def test_PIDController():
    kp, ki, kd, tf = symbols("kp ki kd tf")
    p1 = PIDController(kp, ki, kd, tf)
    p2 = PIDController()

    # Type Checking
    assert isinstance(p1, PIDController)
    assert isinstance(p1, TransferFunction)

    # Properties checking
    assert p1 == PIDController(kp, ki, kd, tf, s)
    assert p2 == PIDController(kp, ki, kd, 0, s)
    assert p1.num == kd*s**2 + ki*s*tf + ki + kp*s**2*tf + kp*s
    assert p1.den == s**2*tf + s
    assert p1.var == s
    assert p1.kp == kp
    assert p1.ki == ki
    assert p1.kd == kd
    assert p1.tf == tf

    # Functionality checking
    assert p1.doit() == TransferFunction(kd*s**2 + ki*s*tf + ki + kp*s**2*tf + kp*s, s**2*tf + s, s)
    assert p1.is_proper == True
    assert p1.is_biproper == True
    assert p1.is_strictly_proper == False
    assert p2.doit() == TransferFunction(kd*s**2 + ki + kp*s, s, s)

    # Using PIDController with TransferFunction
    tf1 = TransferFunction(s, s + 1, s)
    par1 = Parallel(p1, tf1)
    ser1 = Series(p1, tf1)
    fed1 = Feedback(p1, tf1)
    assert par1 == Parallel(PIDController(kp, ki, kd, tf, s), TransferFunction(s, s + 1, s))
    assert ser1 == Series(PIDController(kp, ki, kd, tf, s), TransferFunction(s, s + 1, s))
    assert fed1 == Feedback(PIDController(kp, ki, kd, tf, s), TransferFunction(s, s + 1, s))
    assert par1.doit() == TransferFunction(s*(s**2*tf + s) + (s + 1)*(kd*s**2 + ki*s*tf + ki + kp*s**2*tf + kp*s),
                                           (s + 1)*(s**2*tf + s), s)
    assert ser1.doit() == TransferFunction(s*(kd*s**2 + ki*s*tf + ki + kp*s**2*tf + kp*s),
                                           (s + 1)*(s**2*tf + s), s)
    assert fed1.doit() == TransferFunction((s + 1)*(s**2*tf + s)*(kd*s**2 + ki*s*tf + ki + kp*s**2*tf + kp*s),
                                           (s*(kd*s**2 + ki*s*tf + ki + kp*s**2*tf + kp*s) + (s + 1)*(s**2*tf + s))*(s**2*tf + s), s)

