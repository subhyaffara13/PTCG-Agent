"""
factory/inference_server.py

Centralized batched inference server for MCTS workers.
Collects prediction requests from local/remote threads via a TCP socket,
batches them, runs a single forward pass, and distributes results.
"""
import logging
import threading
import time
import socket
import json
from queue import Queue, Empty
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


class _InferenceRequest:
    """A single inference request with a future-like result."""
    __slots__ = ["state_data", "result_event", "logits", "value"]

    def __init__(self, state_data: dict):
        self.state_data = state_data
        self.result_event = threading.Event()
        self.logits = None
        self.value = None


class InferenceServer:
    def __init__(self, model, device="cpu", batch_size: int = 32, max_wait_ms: int = 10,
                 state_to_tensor=None, state_to_card_tokens=None, port: int = 9999):
        self.model = model
        self.device = device
        self.batch_size = batch_size
        self.max_wait_s = max_wait_ms / 1000.0
        self.state_to_tensor = state_to_tensor
        self.state_to_card_tokens = state_to_card_tokens
        self.port = port
        self.request_queue = Queue()
        self._running = False
        self._thread = None
        self._listener_thread = None
        self._stats = {"total_requests": 0, "total_batches": 0, "avg_batch_size": 0.0}

    def start(self):
        """Start the inference server and TCP listener loop in background threads."""
        if self._running:
            return
        self._running = True
        
        # Start PPO batching loop
        self._thread = threading.Thread(target=self._serve_loop, daemon=True, name="InferenceServer")
        self._thread.start()
        
        # Start TCP listener loop
        self._listener_thread = threading.Thread(target=self._socket_listener_loop, daemon=True, name="InferenceSocketListener")
        self._listener_thread.start()
        
        logger.info(f"InferenceServer started (batch_size={self.batch_size}, max_wait={self.max_wait_s*1000:.0f}ms) on port {self.port}")

    def stop(self):
        """Gracefully stop the server."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        logger.info(f"InferenceServer stopped. Stats: {self._stats}")

    def predict(self, state_data: dict) -> Tuple:
        """Submit a prediction request and block until result is ready.
        Returns (logits_list, value_float). Thread-safe."""
        request = _InferenceRequest(state_data)
        self.request_queue.put(request)
        request.result_event.wait(timeout=5.0)  # 5s timeout safety
        return (request.logits, request.value)

    def _socket_listener_loop(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind(("0.0.0.0", self.port))
            server_socket.listen(128)
            server_socket.settimeout(1.0)
        except Exception as e:
            logger.error(f"InferenceServer socket bind failed on port {self.port}: {e}")
            return

        while self._running:
            try:
                conn, addr = server_socket.accept()
                threading.Thread(target=self._handle_socket_client, args=(conn,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception:
                break
        server_socket.close()

    def _handle_socket_client(self, conn):
        try:
            rfile = conn.makefile('r', encoding='utf-8')
            wfile = conn.makefile('w', encoding='utf-8')
            for line in rfile:
                if not self._running:
                    break
                line = line.strip()
                if not line:
                    continue
                state_data = json.loads(line)
                logits, value = self.predict(state_data)
                response = {"logits": logits, "value": value}
                wfile.write(json.dumps(response) + "\n")
                wfile.flush()
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _serve_loop(self):
        """Main loop: collect requests, batch them, run inference, distribute results."""
        while self._running:
            batch = []
            deadline = time.monotonic() + self.max_wait_s

            # Collect requests up to batch_size or until max_wait
            while len(batch) < self.batch_size:
                remaining = max(0.001, deadline - time.monotonic())
                try:
                    request = self.request_queue.get(timeout=remaining)
                    batch.append(request)
                except Empty:
                    break

            if not batch:
                continue

            # Run batched inference
            try:
                self._run_batch(batch)
            except Exception as e:
                logger.error(f"InferenceServer batch failed: {e}")
                # Set all results to None so waiters don't hang
                for req in batch:
                    req.logits = None
                    req.value = 0.0
                    req.result_event.set()

            # Update stats
            self._stats["total_requests"] += len(batch)
            self._stats["total_batches"] += 1
            self._stats["avg_batch_size"] = (
                self._stats["total_requests"] / max(1, self._stats["total_batches"])
            )

    def _run_batch(self, batch):
        """Process a batch of inference requests."""
        if not HAS_TORCH or self.model is None:
            for req in batch:
                req.logits = None
                req.value = 0.0
                req.result_event.set()
            return

        import torch

        # Try Transformer path first
        use_transformer = self.state_to_card_tokens is not None
        token_batch, zone_batch, scalar_batch, mask_batch = [], [], [], []
        flat_batch = []
        transformer_indices = []
        flat_indices = []

        for i, req in enumerate(batch):
            if use_transformer:
                try:
                    t, z, s, m = self.state_to_card_tokens(req.state_data)
                    if t is not None:
                        token_batch.append(t)
                        zone_batch.append(z)
                        scalar_batch.append(s)
                        mask_batch.append(m)
                        transformer_indices.append(i)
                        continue
                except Exception:
                    pass

            # Fallback to flat tensor
            if self.state_to_tensor is not None:
                try:
                    flat_t = self.state_to_tensor(req.state_data)
                    if flat_t is not None:
                        flat_batch.append(flat_t)
                        flat_indices.append(i)
                        continue
                except Exception:
                    pass

            # No valid tensor - return defaults
            req.logits = None
            req.value = 0.0
            req.result_event.set()

        self.model.eval()
        with torch.no_grad():
            # Process Transformer batch
            if token_batch:
                tokens = torch.cat(token_batch, dim=0).to(self.device)
                zones = torch.cat(zone_batch, dim=0).to(self.device)
                scalars = torch.cat(scalar_batch, dim=0).to(self.device)
                masks = torch.cat(mask_batch, dim=0).to(self.device)
                logits, values = self.model(
                    x=None, token_ids=tokens, zone_ids=zones,
                    scalars=scalars, padding_mask=masks
                )
                for j, idx in enumerate(transformer_indices):
                    batch[idx].logits = logits[j].cpu().tolist()
                    batch[idx].value = values[j].item()
                    batch[idx].result_event.set()

            # Process flat MLP batch
            if flat_batch:
                flat_tensor = torch.cat(flat_batch, dim=0).to(self.device)
                logits, values = self.model(x=flat_tensor)
                for j, idx in enumerate(flat_indices):
                    batch[idx].logits = logits[j].cpu().tolist()
                    batch[idx].value = values[j].item()
                    batch[idx].result_event.set()

    @property
    def stats(self) -> dict:
        return dict(self._stats)
