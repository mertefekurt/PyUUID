import uuid
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict
from dataclasses import dataclass
from statistics import mean, stdev
import math


@dataclass
class DistributionStats:
    total_samples: int
    unique_count: int
    collision_count: int
    collision_rate: float
    entropy: float
    bit_distribution: Dict[int, float]


@dataclass
class UUIDAnalysis:
    uuid_obj: uuid.UUID
    version: int
    variant: str
    bit_entropy: float
    hex_distribution: Dict[str, int]
    bit_patterns: Dict[str, int]


class UUIDAnalyzer:
    _VARIANT_MAP = {
        uuid.RESERVED_NCS: "reserved_ncs",
        uuid.RFC_4122: "rfc_4122",
        uuid.RESERVED_MICROSOFT: "microsoft",
        uuid.RESERVED_FUTURE: "reserved",
    }

    def __init__(self):
        self.analyzed_uuids: List[UUIDAnalysis] = []

    def analyze_uuid(self, uuid_obj: uuid.UUID) -> UUIDAnalysis:
        hex_str = uuid_obj.hex
        hex_dist = Counter(hex_str)
        bit_patterns = self._analyze_bit_patterns(uuid_obj)
        bit_entropy = self._calculate_bit_entropy(uuid_obj)
        variant_str = self._VARIANT_MAP.get(uuid_obj.variant, "unknown")

        analysis = UUIDAnalysis(
            uuid_obj=uuid_obj,
            version=uuid_obj.version,
            variant=variant_str,
            bit_entropy=bit_entropy,
            hex_distribution=dict(hex_dist),
            bit_patterns=bit_patterns,
        )
        self.analyzed_uuids.append(analysis)
        return analysis

    def _analyze_bit_patterns(self, uuid_obj: uuid.UUID) -> Dict[str, int]:
        bits = bin(uuid_obj.int)[2:].zfill(128)
        patterns = {
            "consecutive_zeros": 0,
            "consecutive_ones": 0,
            "alternating": 0,
            "bit_transitions": 0,
        }

        max_zero_run = 0
        max_one_run = 0
        current_zero_run = 0
        current_one_run = 0
        transitions = 0

        for i in range(len(bits)):
            if bits[i] == "0":
                current_zero_run += 1
                max_zero_run = max(max_zero_run, current_zero_run)
                current_one_run = 0
                if i > 0 and bits[i - 1] == "1":
                    transitions += 1
            else:
                current_one_run += 1
                max_one_run = max(max_one_run, current_one_run)
                current_zero_run = 0
                if i > 0 and bits[i - 1] == "0":
                    transitions += 1

        patterns["consecutive_zeros"] = max_zero_run
        patterns["consecutive_ones"] = max_one_run
        patterns["bit_transitions"] = transitions
        return patterns

    def _calculate_bit_entropy(self, uuid_obj: uuid.UUID) -> float:
        hex_str = uuid_obj.hex
        char_freq = Counter(hex_str)
        entropy = 0.0
        length = len(hex_str)

        for count in char_freq.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy

    def analyze_distribution(self, uuids: List[uuid.UUID]) -> DistributionStats:
        unique_uuids = set()
        collisions = 0
        bit_distributions = defaultdict(list)

        for u in uuids:
            uuid_str = str(u)
            if uuid_str in unique_uuids:
                collisions += 1
            else:
                unique_uuids.add(uuid_str)

            analysis = self.analyze_uuid(u)
            for bit_pos in range(128):
                bit_value = (u.int >> (127 - bit_pos)) & 1
                bit_distributions[bit_pos].append(bit_value)

        total = len(uuids)
        unique_count = len(unique_uuids)
        collision_rate = collisions / total if total > 0 else 0.0

        bit_stats = {}
        for bit_pos, values in bit_distributions.items():
            bit_stats[bit_pos] = mean(values)

        overall_entropy = mean([a.bit_entropy for a in self.analyzed_uuids[-total:]])

        return DistributionStats(
            total_samples=total,
            unique_count=unique_count,
            collision_count=collisions,
            collision_rate=collision_rate,
            entropy=overall_entropy,
            bit_distribution=bit_stats,
        )

    def detect_anomalies(self, threshold: float = 2.0) -> List[Tuple[uuid.UUID, str]]:
        if len(self.analyzed_uuids) < 10:
            return []

        entropies = [a.bit_entropy for a in self.analyzed_uuids]
        mean_entropy = mean(entropies)
        std_entropy = stdev(entropies) if len(entropies) > 1 else 0

        anomalies = []
        for analysis in self.analyzed_uuids:
            z_score = (
                (analysis.bit_entropy - mean_entropy) / std_entropy
                if std_entropy > 0
                else 0
            )
            if abs(z_score) > threshold:
                anomalies.append(
                    (analysis.uuid_obj, f"entropy_z_score: {z_score:.2f}")
                )

        return anomalies

    def get_version_distribution(self) -> Dict[int, int]:
        version_dist = Counter(a.version for a in self.analyzed_uuids)
        return dict(version_dist)

    def get_variant_distribution(self) -> Dict[str, int]:
        variant_dist = Counter(a.variant for a in self.analyzed_uuids)
        return dict(variant_dist)

    def generate_report(self) -> str:
        if not self.analyzed_uuids:
            return "No UUIDs analyzed"

        report = ["UUID Analysis Report", "=" * 60]
        report.append(f"Total UUIDs analyzed: {len(self.analyzed_uuids)}")

        version_dist = self.get_version_distribution()
        report.append(f"\nVersion distribution: {version_dist}")

        variant_dist = self.get_variant_distribution()
        report.append(f"Variant distribution: {variant_dist}")

        avg_entropy = mean([a.bit_entropy for a in self.analyzed_uuids])
        report.append(f"\nAverage bit entropy: {avg_entropy:.4f}")

        anomalies = self.detect_anomalies()
        if anomalies:
            report.append(f"\nAnomalies detected: {len(anomalies)}")
            for uuid_obj, reason in anomalies[:5]:
                report.append(f"  {uuid_obj}: {reason}")

        return "\n".join(report)


if __name__ == "__main__":
    analyzer = UUIDAnalyzer()
    test_uuids = [uuid.uuid4() for _ in range(1000)]
    stats = analyzer.analyze_distribution(test_uuids)
    print(analyzer.generate_report())
    print(f"\nDistribution Stats:")
    print(f"Unique: {stats.unique_count}/{stats.total_samples}")
    print(f"Collision rate: {stats.collision_rate:.6f}")

