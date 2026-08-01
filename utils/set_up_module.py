
def setUpModule():
  fake.set_n_cpu_devices()


def setUpModule():
  fake.set_n_cpu_devices()
  asserts.assert_devices_available(
      FLAGS['chex_n_cpu_devices'].value, 'cpu', backend='cpu')

