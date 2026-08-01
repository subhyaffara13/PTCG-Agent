
def test_inverse_symbolic_float_issue_26821():
    Tau, Tau_syn_in, Tau_syn_ex, C_m, Tau_syn_gap = symbols("Tau Tau_syn_in Tau_syn_ex C_m Tau_syn_gap")
    __h = symbols("__h")

    M = Matrix([
        [0,0,0,0,0,(1.0*Tau*__h-1.0*Tau_syn_in*__h)/(2.0*Tau-1.0*Tau_syn_in),-1.0*Tau*Tau_syn_in/(2.0*Tau-1.0*Tau_syn_in)],
        [0,0,0,0,0,(-1.0*Tau*__h+1.0*Tau_syn_in*__h)/(2.0*Tau*Tau_syn_in-1.0*Tau_syn_in**2),1.0],
        [0,(1.0*Tau*__h-1.0*Tau_syn_ex*__h)/(2.0*Tau-1.0*Tau_syn_ex),-1.0*Tau*Tau_syn_ex/(2.0*Tau-1.0*Tau_syn_ex),0,0,0,0],
        [0,(-1.0*Tau*__h+1.0*Tau_syn_ex*__h)/(2.0*Tau*Tau_syn_ex-1.0*Tau_syn_ex**2),1.0,0,0,0,0],
        [0,0,0,(1.0*Tau*__h-1.0*Tau_syn_gap*__h)/(2.0*Tau-1.0*Tau_syn_gap),-1.0*Tau*Tau_syn_gap/(2.0*Tau-1.0*Tau_syn_gap),0,0],
        [0,0,0,(-1.0*Tau*__h+1.0*Tau_syn_gap*__h)/(2.0*Tau*Tau_syn_gap-1.0*Tau_syn_gap**2),1.0,0,0],
        [1.0,-1.0*Tau*Tau_syn_ex*__h/(2.0*C_m*Tau-1.0*C_m*Tau_syn_ex),0,-1.0*Tau*Tau_syn_gap*__h/(2.0*C_m*Tau-1.0*C_m*Tau_syn_gap),0,-1.0*Tau*Tau_syn_in*__h/(2.0*C_m*Tau-1.0*C_m*Tau_syn_in),0]
    ])

    Mi = M.inv()

    assert (M*Mi - eye(7)).applyfunc(cancel) == zeros(7)

    # https://github.com/sympy/sympy/issues/26821
    # Previously very large floats were in the result.
    assert max(abs(f) for f in Mi.atoms(Float)) < 1e3

