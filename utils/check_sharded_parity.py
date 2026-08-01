
def check_sharded_parity(
    cls,  # unit test class
    replicated_module: nn.Module,
    sharded_module: nn.Module,
    prefixes_to_ignore: tuple[str, ...] = (),
):
    for (replicated_name, replicated_param), (sharded_name, sharded_param) in zip(
        replicated_module.named_parameters(),
        sharded_module.named_parameters(),
        strict=True,
    ):
        clean_sharded_name = sharded_name
        for prefix in prefixes_to_ignore:
            clean_sharded_name = clean_sharded_name.replace(prefix, "")
        cls.assertEqual(replicated_name, clean_sharded_name)
        cls.assertIsInstance(sharded_param, DTensor)
        if not isinstance(sharded_param, DTensor):
            raise AssertionError("Expected sharded_param to be a DTensor")  # mypy
        mesh, placements = sharded_param.device_mesh, sharded_param.placements
        if tuple(placements) == (Shard(0), Shard(0)):
            raise AssertionError(
                "FSDP's (Shard(0), Shard(0)) layout differs from distribute_tensor(), "
                "so we cannot check for equality using it"
            )
        sharded_ref_param = distribute_tensor(replicated_param, mesh, placements)
        cls.assertEqual(sharded_param.to_local(), sharded_ref_param.to_local())
        if replicated_param.grad is None:
            cls.assertIsNone(sharded_param.grad)
            continue
        cls.assertIsNotNone(sharded_param.grad)
        sharded_ref_grad = distribute_tensor(replicated_param.grad, mesh, placements)
        cls.assertIsInstance(sharded_param.grad, DTensor)
        if not isinstance(sharded_param.grad, DTensor):
            raise AssertionError("Expected sharded_param.grad to be a DTensor")  # mypy
        cls.assertEqual(sharded_param.grad.to_local(), sharded_ref_grad.to_local())

