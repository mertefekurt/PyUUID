import uuid
from typing import Optional, Dict, List, Tuple, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class UUIDVersion(Enum):
    V1 = 1
    V3 = 3
    V4 = 4
    V5 = 5


@dataclass
class MigrationResult:
    source_uuid: uuid.UUID
    target_uuid: uuid.UUID
    migration_type: str
    success: bool
    timestamp: datetime
    metadata: Optional[Dict] = None


class UUIDMigrator:
    def __init__(self):
        self.migration_history: List[MigrationResult] = []
        self.namespace_cache: Dict[str, uuid.UUID] = {}

    def get_namespace(self, namespace_name: str) -> uuid.UUID:
        if namespace_name not in self.namespace_cache:
            self.namespace_cache[namespace_name] = uuid.uuid5(
                uuid.NAMESPACE_DNS, namespace_name
            )
        return self.namespace_cache[namespace_name]

    def migrate_v4_to_v5(
        self, source_uuid: uuid.UUID, namespace: str, name: str
    ) -> MigrationResult:
        if not isinstance(namespace, str) or not isinstance(name, str):
            return MigrationResult(
                source_uuid=source_uuid,
                target_uuid=source_uuid,
                migration_type="v4_to_v5",
                success=False,
                timestamp=datetime.now(),
                metadata={"error": "namespace and name must be strings"},
            )
        try:
            namespace_uuid = self.get_namespace(namespace)
            target_uuid = uuid.uuid5(namespace_uuid, name)
            result = MigrationResult(
                source_uuid=source_uuid,
                target_uuid=target_uuid,
                migration_type="v4_to_v5",
                success=True,
                timestamp=datetime.now(),
                metadata={"namespace": namespace, "name": name},
            )
            self.migration_history.append(result)
            return result
        except Exception as e:
            return MigrationResult(
                source_uuid=source_uuid,
                target_uuid=source_uuid,
                migration_type="v4_to_v5",
                success=False,
                timestamp=datetime.now(),
                metadata={"error": str(e)},
            )

    def migrate_v5_to_v3(
        self, source_uuid: uuid.UUID, namespace: str, name: str
    ) -> MigrationResult:
        if not isinstance(namespace, str) or not isinstance(name, str):
            return MigrationResult(
                source_uuid=source_uuid,
                target_uuid=source_uuid,
                migration_type="v5_to_v3",
                success=False,
                timestamp=datetime.now(),
                metadata={"error": "namespace and name must be strings"},
            )
        try:
            namespace_uuid = self.get_namespace(namespace)
            target_uuid = uuid.uuid3(namespace_uuid, name)
            result = MigrationResult(
                source_uuid=source_uuid,
                target_uuid=target_uuid,
                migration_type="v5_to_v3",
                success=True,
                timestamp=datetime.now(),
                metadata={"namespace": namespace, "name": name},
            )
            self.migration_history.append(result)
            return result
        except Exception as e:
            return MigrationResult(
                source_uuid=source_uuid,
                target_uuid=source_uuid,
                migration_type="v5_to_v3",
                success=False,
                timestamp=datetime.now(),
                metadata={"error": str(e)},
            )

    def preserve_identity_migration(
        self, source_uuid: uuid.UUID, target_version: UUIDVersion
    ) -> Optional[MigrationResult]:
        if target_version == UUIDVersion.V4:
            new_uuid = uuid.uuid4()
            result = MigrationResult(
                source_uuid=source_uuid,
                target_uuid=new_uuid,
                migration_type="identity_preserve",
                success=True,
                timestamp=datetime.now(),
                metadata={"source_version": source_uuid.version, "target_version": 4},
            )
            self.migration_history.append(result)
            return result
        return None

    def batch_migrate(
        self, uuids: List[uuid.UUID], migration_func: Callable, *args, **kwargs
    ) -> List[MigrationResult]:
        if not isinstance(uuids, list) or not all(isinstance(u, uuid.UUID) for u in uuids):
            raise ValueError("uuids must be a list of UUID objects")
        if not callable(migration_func):
            raise ValueError("migration_func must be callable")
        results = []
        for u in uuids:
            result = migration_func(u, *args, **kwargs)
            results.append(result)
        return results

    def get_migration_statistics(self) -> Dict:
        total = len(self.migration_history)
        successful = sum(1 for r in self.migration_history if r.success)
        failed = total - successful
        by_type = {}
        for result in self.migration_history:
            by_type[result.migration_type] = by_type.get(result.migration_type, 0) + 1
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "by_type": by_type,
        }

    def rollback_migration(self, result: MigrationResult) -> bool:
        if result in self.migration_history:
            self.migration_history.remove(result)
            return True
        return False

    def clear_history(self):
        self.migration_history.clear()
        self.namespace_cache.clear()


if __name__ == "__main__":
    migrator = UUIDMigrator()
    test_uuid = uuid.uuid4()
    result = migrator.migrate_v4_to_v5(test_uuid, "example.com", "user123")
    print(f"Migration: {result.source_uuid} -> {result.target_uuid}")
    print(f"Success: {result.success}")
    stats = migrator.get_migration_statistics()
    print(f"Statistics: {stats}")

