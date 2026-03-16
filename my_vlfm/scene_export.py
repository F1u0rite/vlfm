import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .semantic_map import SemanticMap


@dataclass(frozen=True)
class MapMetadata:
    scene_name: str
    map_height: int
    map_width: int
    cell_size_m: float
    origin_world: Tuple[float, float, float]
    grid_to_world: Dict[str, str]
    occupancy_label_def: Dict[int, str]


@dataclass(frozen=True)
class SceneExportBundle:
    occupancy_map: np.ndarray
    semantic_map: SemanticMap
    metadata: MapMetadata


def load_scene_export(scene_export_dir: str) -> SceneExportBundle:
    metadata = load_map_metadata(os.path.join(scene_export_dir, "map_metadata.json"))
    occupancy_map = np.load(os.path.join(scene_export_dir, "occupancy_map.npy"))
    semantic_map = load_semantic_map(scene_export_dir, metadata)
    return SceneExportBundle(occupancy_map=occupancy_map, semantic_map=semantic_map, metadata=metadata)


def load_map_metadata(path: str) -> MapMetadata:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    occ_label_def = {int(k): str(v) for k, v in data["occupancy_label_def"].items()}
    return MapMetadata(
        scene_name=str(data.get("scene_name", "unknown_scene")),
        map_height=int(data["map_height"]),
        map_width=int(data["map_width"]),
        cell_size_m=float(data["cell_size_m"]),
        origin_world=tuple(data.get("origin_world", [0.0, 0.0, 0.0])),  # type: ignore[arg-type]
        grid_to_world=dict(data.get("grid_to_world", {"row_axis": "z", "col_axis": "x"})),
        occupancy_label_def=occ_label_def,
    )


def load_semantic_map(scene_export_dir: str, metadata: MapMetadata) -> SemanticMap:
    objects_path = os.path.join(scene_export_dir, "semantic_objects.json")
    points_path = os.path.join(scene_export_dir, "semantic_points.json")

    records: List[dict] = []
    if os.path.isfile(objects_path):
        with open(objects_path, "r", encoding="utf-8") as f:
            objects_payload = json.load(f)
        for obj in objects_payload.get("objects", []):
            label = str(obj["label"]).lower().strip()
            grid_pixels = obj.get("grid_pixels", [])
            if not grid_pixels and "grid_centroid" in obj:
                grid_pixels = [obj["grid_centroid"]]
            world_points = [_grid_to_xy(p, metadata) for p in grid_pixels]
            if len(world_points) > 0:
                records.append({"category": label, "points": world_points})

    if len(records) == 0 and os.path.isfile(points_path):
        with open(points_path, "r", encoding="utf-8") as f:
            points_payload = json.load(f)
        grouped: Dict[str, List[Tuple[float, float]]] = {}
        for pt in points_payload.get("points", []):
            label = str(pt["label"]).lower().strip()
            xy = _grid_to_xy(pt["grid"], metadata)
            grouped.setdefault(label, []).append(xy)
        for label, pts in grouped.items():
            records.append({"category": label, "points": pts})

    return SemanticMap.from_records(records)


def infer_occupancy_labels(metadata: MapMetadata) -> Tuple[int, int]:
    """Return (free_value, unknown_value) from occupancy_label_def."""
    free_value = None
    unknown_value = None
    for k, v in metadata.occupancy_label_def.items():
        lv = v.lower()
        if lv == "free":
            free_value = k
        elif lv == "unknown":
            unknown_value = k

    if free_value is None:
        raise ValueError("occupancy_label_def must include a label mapped to 'free'.")
    if unknown_value is None:
        unknown_value = 2
    return free_value, unknown_value


def _grid_to_xy(grid_rc: Sequence[float], metadata: MapMetadata) -> Tuple[float, float]:
    row = float(grid_rc[0])
    col = float(grid_rc[1])
    x = float(metadata.origin_world[0]) + col * metadata.cell_size_m
    y = float(metadata.origin_world[2]) + row * metadata.cell_size_m
    return x, y
