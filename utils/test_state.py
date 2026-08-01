
def test_state():
    x = symbols('x')
    bra = Bra()
    ket = Ket()
    bra_tall = Bra(x/2)
    ket_tall = Ket(x/2)
    tbra = TimeDepBra()
    tket = TimeDepKet()
    assert str(bra) == '<psi|'
    assert pretty(bra) == '<psi|'
    assert upretty(bra) == '⟨ψ❘'
    assert latex(bra) == r'{\left\langle \psi\right|}'
    sT(bra, "Bra(Symbol('psi'))")
    assert str(ket) == '|psi>'
    assert pretty(ket) == '|psi>'
    assert upretty(ket) == '❘ψ⟩'
    assert latex(ket) == r'{\left|\psi\right\rangle }'
    sT(ket, "Ket(Symbol('psi'))")
    assert str(bra_tall) == '<x/2|'
    ascii_str = \
"""\
 / |\n\
/ x|\n\
\\ -|\n\
 \\2|\
"""
    ucode_str = \
"""\
 ╱ │\n\
╱ x│\n\
╲ ─│\n\
 ╲2│\
"""
    assert pretty(bra_tall) == ascii_str
    assert upretty(bra_tall) == ucode_str
    assert latex(bra_tall) == r'{\left\langle \frac{x}{2}\right|}'
    sT(bra_tall, "Bra(Mul(Rational(1, 2), Symbol('x')))")
    assert str(ket_tall) == '|x/2>'
    ascii_str = \
"""\
| \\ \n\
|x \\\n\
|- /\n\
|2/ \
"""
    ucode_str = \
"""\
│ ╲ \n\
│x ╲\n\
│─ ╱\n\
│2╱ \
"""
    assert pretty(ket_tall) == ascii_str
    assert upretty(ket_tall) == ucode_str
    assert latex(ket_tall) == r'{\left|\frac{x}{2}\right\rangle }'
    sT(ket_tall, "Ket(Mul(Rational(1, 2), Symbol('x')))")
    assert str(tbra) == '<psi;t|'
    assert pretty(tbra) == '<psi;t|'
    assert upretty(tbra) == '⟨ψ;t❘'
    assert latex(tbra) == r'{\left\langle \psi;t\right|}'
    sT(tbra, "TimeDepBra(Symbol('psi'),Symbol('t'))")
    assert str(tket) == '|psi;t>'
    assert pretty(tket) == '|psi;t>'
    assert upretty(tket) == '❘ψ;t⟩'
    assert latex(tket) == r'{\left|\psi;t\right\rangle }'
    sT(tket, "TimeDepKet(Symbol('psi'),Symbol('t'))")


def test_state(env, num_cycles):
    graphical_envs = ["knights_archers_zombies_v10"]
    env.reset()
    state_0 = env.state()
    for agent in env.agent_iter(env.num_agents * num_cycles):
        observation, reward, terminated, truncated, info = env.last(observe=False)
        if terminated or truncated:
            action = None
        else:
            action = env.action_space(agent).sample()

        env.step(action)
        new_state = env.state()
        assert env.state_space.contains(
            new_state
        ), "Environment's state is outside of it's state space"
        if (
            not isinstance(new_state, np.ndarray)
            and str(env.unwrapped) not in graphical_envs
        ):
            warnings.warn("State is not NumPy array")
            return
        if np.isinf(new_state).any():
            warnings.warn(
                "State contains infinity (np.inf) or negative infinity (-np.inf)"
            )
        if np.isnan(new_state).any():
            warnings.warn("State contains NaNs")
        if len(new_state.shape) > 3:
            warnings.warn("State has more than 3 dimensions")
        if new_state.shape == (0,):
            assert False, "State can not be an empty array"
        if new_state.shape == (1,):
            warnings.warn("State is a single number")
        if not isinstance(new_state, state_0.__class__):
            warnings.warn("State between Observations are different classes")
        if (new_state.shape != state_0.shape) and (
            len(new_state.shape) == len(state_0.shape)
        ):
            warnings.warn("States are different shapes")
        if len(new_state.shape) != len(state_0.shape):
            warnings.warn("States have different number of dimensions")
        if not np.can_cast(new_state.dtype, np.dtype("float64")):
            warnings.warn("State numpy array is not a numeric dtype")
        if np.array_equal(new_state, np.zeros(new_state.shape)):
            warnings.warn("State numpy array is all zeros.")
        if (
            not np.all(new_state >= 0)
            and (
                (len(new_state.shape) == 2)
                or (len(new_state.shape) == 3 and new_state.shape[2] == 1)
                or (len(new_state.shape) == 3 and new_state.shape[2] == 3)
            )
            and str(env.unwrapped) not in graphical_envs
        ):
            warnings.warn(
                "The state contains negative numbers and is in the shape of a graphical observation. This might be a bad thing."
            )

