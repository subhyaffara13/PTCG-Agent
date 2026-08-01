
def force_slow_sim(monkeypatch):
    monkeypatch.setenv("FAST_SIM_MODE", "false")

