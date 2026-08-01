
def has_torchvision_roi_align() -> bool:
    try:
        from torchvision.ops import roi_align  # noqa: F401

        torch._C._dispatch_has_kernel_for_dispatch_key("torchvision::nms", "Meta")
        return roi_align is not None and hasattr(
            getattr(torch.ops, "torchvision", None), "roi_align"
        )
    except ImportError:
        return False
    except RuntimeError as e:
        assert "torchvision::nms does not exist" in str(e)
        return False

