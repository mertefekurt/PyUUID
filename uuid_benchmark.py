import uuid
import time
import statistics
from typing import Dict, List, Callable
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    function_name: str
    iterations: int
    total_time: float
    average_time: float
    min_time: float
    max_time: float
    median_time: float
    std_deviation: float
    operations_per_second: float


class UUIDBenchmark:
    def __init__(self):
        self.results: Dict[str, BenchmarkResult] = {}

    def measure_function(
        self, func: Callable, iterations: int = 10000, *args, **kwargs
    ) -> BenchmarkResult:
        if not isinstance(iterations, int) or iterations < 1:
            raise ValueError("iterations must be a positive integer")
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append((end - start) * 1000000)

        total_time = sum(times)
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        median_time = statistics.median(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
        ops_per_sec = (iterations / total_time) * 1000000 if total_time > 0 else 0

        result = BenchmarkResult(
            function_name=func.__name__,
            iterations=iterations,
            total_time=total_time / 1000,
            average_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            median_time=median_time,
            std_deviation=std_dev,
            operations_per_second=ops_per_sec,
        )
        self.results[func.__name__] = result
        return result

    def compare_versions(self, iterations: int = 10000) -> Dict[str, BenchmarkResult]:
        def generate_v1():
            return uuid.uuid1()

        def generate_v3():
            return uuid.uuid3(uuid.NAMESPACE_DNS, "test")

        def generate_v4():
            return uuid.uuid4()

        def generate_v5():
            return uuid.uuid5(uuid.NAMESPACE_DNS, "test")

        results = {}
        for func in [generate_v1, generate_v3, generate_v4, generate_v5]:
            result = self.measure_function(func, iterations)
            results[func.__name__] = result

        return results

    def benchmark_conversions(self, iterations: int = 10000) -> Dict[str, BenchmarkResult]:
        test_uuid = uuid.uuid4()

        def to_string():
            return str(test_uuid)

        def to_hex():
            return test_uuid.hex

        def to_int():
            return test_uuid.int

        def to_bytes():
            return test_uuid.bytes

        def from_string():
            return uuid.UUID(str(test_uuid))

        def from_hex():
            return uuid.UUID(test_uuid.hex)

        results = {}
        for func in [to_string, to_hex, to_int, to_bytes, from_string, from_hex]:
            result = self.measure_function(func, iterations)
            results[func.__name__] = result

        return results

    def benchmark_validation(self, iterations: int = 10000) -> Dict[str, BenchmarkResult]:
        valid_uuid_str = str(uuid.uuid4())
        invalid_uuid_str = "not-a-uuid"

        def validate_valid():
            try:
                uuid.UUID(valid_uuid_str)
                return True
            except ValueError:
                return False

        def validate_invalid():
            try:
                uuid.UUID(invalid_uuid_str)
                return True
            except ValueError:
                return False

        results = {}
        for func in [validate_valid, validate_invalid]:
            result = self.measure_function(func, iterations)
            results[func.__name__] = result

        return results

    def get_comparison_report(self) -> str:
        if not self.results:
            return "No benchmark results available"

        report = ["UUID Benchmark Comparison Report", "=" * 60]
        sorted_results = sorted(
            self.results.values(), key=lambda x: x.average_time
        )

        for result in sorted_results:
            report.append(f"\n{result.function_name}:")
            report.append(f"  Average: {result.average_time:.4f} μs")
            report.append(f"  Median: {result.median_time:.4f} μs")
            report.append(f"  Min: {result.min_time:.4f} μs")
            report.append(f"  Max: {result.max_time:.4f} μs")
            report.append(f"  Std Dev: {result.std_deviation:.4f} μs")
            report.append(f"  Ops/sec: {result.operations_per_second:,.0f}")

        return "\n".join(report)

    def clear_results(self):
        self.results.clear()


if __name__ == "__main__":
    benchmark = UUIDBenchmark()
    print("Benchmarking UUID versions...")
    version_results = benchmark.compare_versions(iterations=50000)
    print("\nBenchmarking UUID conversions...")
    conversion_results = benchmark.benchmark_conversions(iterations=50000)
    print("\n" + benchmark.get_comparison_report())

