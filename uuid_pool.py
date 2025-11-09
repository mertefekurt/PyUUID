import uuid
import threading
import time
from typing import Optional, List, Dict
from dataclasses import dataclass
from queue import Queue, Empty
from collections import deque
import weakref


@dataclass
class PoolConfig:
    min_size: int = 10
    max_size: int = 1000
    prefill: bool = True
    refill_threshold: float = 0.3
    refill_batch_size: int = 50
    ttl_seconds: Optional[float] = None


@dataclass
class PoolStats:
    current_size: int
    total_generated: int
    total_consumed: int
    cache_hits: int
    cache_misses: int
    refill_count: int
    eviction_count: int


class UUIDPool:
    def __init__(self, config: Optional[PoolConfig] = None):
        self.config = config or PoolConfig()
        self.pool: Queue = Queue(maxsize=self.config.max_size)
        self.stats = PoolStats(
            current_size=0,
            total_generated=0,
            total_consumed=0,
            cache_hits=0,
            cache_misses=0,
            refill_count=0,
            eviction_count=0,
        )
        self.lock = threading.Lock()
        self._uuid_timestamps: Dict[str, float] = {}
        self._running = True

        if self.config.prefill:
            self._prefill_pool()

        self._start_refill_thread()

    def _prefill_pool(self):
        for _ in range(self.config.min_size):
            self._generate_and_add()

    def _generate_and_add(self) -> bool:
        try:
            new_uuid = uuid.uuid4()
            uuid_str = str(new_uuid)
            self.pool.put_nowait(new_uuid)
            self._uuid_timestamps[uuid_str] = time.time()
            with self.lock:
                self.stats.total_generated += 1
                self.stats.current_size = self.pool.qsize()
            return True
        except:
            return False

    def _start_refill_thread(self):
        def refill_worker():
            while self._running:
                try:
                    current_size = self.pool.qsize()
                    threshold = int(self.config.max_size * self.config.refill_threshold)

                    if current_size < threshold:
                        needed = min(
                            self.config.refill_batch_size,
                            self.config.max_size - current_size,
                        )
                        for _ in range(needed):
                            self._generate_and_add()
                        with self.lock:
                            self.stats.refill_count += 1

                    if self.config.ttl_seconds:
                        self._evict_expired()

                    time.sleep(0.1)
                except Exception:
                    pass

        thread = threading.Thread(target=refill_worker, daemon=True)
        thread.start()

    def _evict_expired(self):
        if not self.config.ttl_seconds:
            return

        current_time = time.time()
        expired = [
            uuid_str
            for uuid_str, timestamp in self._uuid_timestamps.items()
            if current_time - timestamp > self.config.ttl_seconds
        ]

        temp_queue = Queue()
        evicted_count = 0

        try:
            while True:
                item = self.pool.get_nowait()
                if str(item) not in expired:
                    temp_queue.put_nowait(item)
                else:
                    evicted_count += 1
                    self._uuid_timestamps.pop(str(item), None)
        except Empty:
            pass

        while not temp_queue.empty():
            self.pool.put_nowait(temp_queue.get())

        with self.lock:
            self.stats.eviction_count += evicted_count
            self.stats.current_size = self.pool.qsize()

    def get(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        try:
            uuid_obj = self.pool.get(timeout=timeout)
            uuid_str = str(uuid_obj)
            self._uuid_timestamps.pop(uuid_str, None)
            with self.lock:
                self.stats.total_consumed += 1
                self.stats.cache_hits += 1
                self.stats.current_size = self.pool.qsize()
            return uuid_obj
        except Empty:
            with self.lock:
                self.stats.cache_misses += 1
            return None

    def get_batch(self, count: int, timeout: Optional[float] = None) -> List[uuid.UUID]:
        results = []
        for _ in range(count):
            uuid_obj = self.get(timeout=timeout)
            if uuid_obj:
                results.append(uuid_obj)
            else:
                break
        return results

    def put(self, uuid_obj: uuid.UUID) -> bool:
        try:
            if self.pool.qsize() < self.config.max_size:
                self.pool.put_nowait(uuid_obj)
                self._uuid_timestamps[str(uuid_obj)] = time.time()
                with self.lock:
                    self.stats.current_size = self.pool.qsize()
                return True
            return False
        except:
            return False

    def get_stats(self) -> PoolStats:
        with self.lock:
            self.stats.current_size = self.pool.qsize()
            return PoolStats(
                current_size=self.stats.current_size,
                total_generated=self.stats.total_generated,
                total_consumed=self.stats.total_consumed,
                cache_hits=self.stats.cache_hits,
                cache_misses=self.stats.cache_misses,
                refill_count=self.stats.refill_count,
                eviction_count=self.stats.eviction_count,
            )

    def clear(self):
        while not self.pool.empty():
            try:
                self.pool.get_nowait()
            except Empty:
                break
        self._uuid_timestamps.clear()
        with self.lock:
            self.stats.current_size = 0

    def shutdown(self):
        self._running = False
        self.clear()


class UUIDPoolManager:
    def __init__(self):
        self.pools: Dict[str, UUIDPool] = {}
        self.lock = threading.Lock()

    def get_pool(self, name: str, config: Optional[PoolConfig] = None) -> UUIDPool:
        with self.lock:
            if name not in self.pools:
                self.pools[name] = UUIDPool(config)
            return self.pools[name]

    def remove_pool(self, name: str):
        with self.lock:
            if name in self.pools:
                self.pools[name].shutdown()
                del self.pools[name]

    def get_all_stats(self) -> Dict[str, PoolStats]:
        with self.lock:
            return {name: pool.get_stats() for name, pool in self.pools.items()}


if __name__ == "__main__":
    config = PoolConfig(min_size=20, max_size=100, prefill=True)
    pool = UUIDPool(config)
    print("Pool initialized")

    uuids = pool.get_batch(10)
    print(f"Retrieved {len(uuids)} UUIDs")

    stats = pool.get_stats()
    print(f"Pool stats: {stats}")

    pool.shutdown()

