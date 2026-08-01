
def test_noncopyable_containers():
    # std::vector
    vnc = m.get_vnc(5)
    for i in range(0, 5):
        assert vnc[i].value == i + 1

    for i, j in enumerate(vnc, start=1):
        assert j.value == i

    # std::deque
    dnc = m.get_dnc(5)
    for i in range(0, 5):
        assert dnc[i].value == i + 1

    i = 1
    for j in dnc:
        assert j.value == i
        i += 1

    # std::map
    mnc = m.get_mnc(5)
    for i in range(1, 6):
        assert mnc[i].value == 10 * i

    vsum = 0
    for k, v in mnc.items():
        assert v.value == 10 * k
        vsum += v.value

    assert vsum == 150

    # std::unordered_map
    mnc = m.get_umnc(5)
    for i in range(1, 6):
        assert mnc[i].value == 10 * i

    vsum = 0
    for k, v in mnc.items():
        assert v.value == 10 * k
        vsum += v.value

    assert vsum == 150

    # nested std::map<std::vector>
    nvnc = m.get_nvnc(5)
    for i in range(1, 6):
        for j in range(0, 5):
            assert nvnc[i][j].value == j + 1

    # Note: maps do not have .values()
    for _, v in nvnc.items():
        for i, j in enumerate(v, start=1):
            assert j.value == i

    # nested std::map<std::map>
    nmnc = m.get_nmnc(5)
    for i in range(1, 6):
        for j in range(10, 60, 10):
            assert nmnc[i][j].value == 10 * j

    vsum = 0
    for _, v_o in nmnc.items():
        for k_i, v_i in v_o.items():
            assert v_i.value == 10 * k_i
            vsum += v_i.value

    assert vsum == 7500

    # nested std::unordered_map<std::unordered_map>
    numnc = m.get_numnc(5)
    for i in range(1, 6):
        for j in range(10, 60, 10):
            assert numnc[i][j].value == 10 * j

    vsum = 0
    for _, v_o in numnc.items():
        for k_i, v_i in v_o.items():
            assert v_i.value == 10 * k_i
            vsum += v_i.value

    assert vsum == 7500

