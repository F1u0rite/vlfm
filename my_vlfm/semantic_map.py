from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np


@dataclass(frozen=True)
class SemanticRegion:
    """A semantic region represented in map coordinates (meters)."""

    category: str
    points: np.ndarray

    @property
    def centroid(self) -> np.ndarray:
        return self.points.mean(axis=0)


class SemanticMap:
    """Minimal VLMaps-like semantic query interface.

    The map stores category-labeled point sets and supports category filtering plus
    simple spatial relation filtering.
    """

    def __init__(self, regions: Sequence[SemanticRegion]) -> None:
        self._regions = list(regions)

    @classmethod
    def from_records(cls, records: Iterable[dict]) -> "SemanticMap":
        regions: List[SemanticRegion] = []
        for rec in records:
            category = str(rec["category"]).lower().strip()
            points = np.asarray(rec["points"], dtype=np.float32)
            if points.ndim != 2 or points.shape[1] != 2:
                raise ValueError("Each semantic region must contain Nx2 map points.")
            regions.append(SemanticRegion(category=category, points=points))
        return cls(regions)

    def query(self, category: str) -> List[SemanticRegion]:
        category = category.lower().strip()
        return [r for r in self._regions if r.category == category]

    def query_with_relation(
        self,
        target_category: str,
        relation: Optional[str],
        reference_category: Optional[str],
        near_threshold_m: float = 1.5,
    ) -> List[SemanticRegion]:
        targets = self.query(target_category)
        if relation is None:
            return targets
        if relation != "near" or reference_category is None:
            return []

        refs = self.query(reference_category)
        if not refs:
            return []

        ref_centers = np.stack([r.centroid for r in refs], axis=0)
        filtered: List[SemanticRegion] = []
        for t in targets:
            t_center = t.centroid
            dists = np.linalg.norm(ref_centers - t_center, axis=1)
            if float(np.min(dists)) <= near_threshold_m:
                filtered.append(t)
        return filtered

    def nearest_region(
        self,
        regions: Sequence[SemanticRegion],
        robot_xy: Tuple[float, float],
    ) -> Optional[SemanticRegion]:
        if not regions:
            return None
        robot = np.asarray(robot_xy, dtype=np.float32)
        distances = [float(np.linalg.norm(r.centroid - robot)) for r in regions]
        return regions[int(np.argmin(distances))]
