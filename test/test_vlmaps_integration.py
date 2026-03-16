import importlib
import json
from pathlib import Path

import numpy as np

from my_vlfm import (
    NavigationState,
    NavigationStateMachine,
    SemanticMap,
    infer_occupancy_labels,
    load_scene_export,
)
from my_vlfm.language_parser import LanguageParser


def test_language_parser_basic_and_relational() -> None:
    parser = LanguageParser()

    parsed = parser.parse("Go to the chair")
    assert parsed.target_object == "chair"
    assert parsed.relation is None

    parsed_rel = parser.parse("Move to the chair near the door")
    assert parsed_rel.target_object == "chair"
    assert parsed_rel.relation == "near"
    assert parsed_rel.reference_object == "door"


def test_navigation_state_machine_path_planned() -> None:
    # legacy style: 0 free, 1 obstacle
    grid = np.zeros((20, 20), dtype=np.uint8)
    grid[8:12, 8:12] = 1

    semantic_map = SemanticMap.from_records(
        [
            {"category": "chair", "points": [[1.4, 1.4], [1.5, 1.5], [1.6, 1.4]]},
            {"category": "door", "points": [[1.9, 1.4], [2.0, 1.5], [2.1, 1.4]]},
        ]
    )

    sm = NavigationStateMachine(
        semantic_map=semantic_map,
        occupancy_grid=grid,
        meters_per_cell=0.1,
        free_value=0,
        unknown_value=2,
    )
    result = sm.run("go to the chair near the door", robot_xy=(0.2, 0.2))

    assert result.state == NavigationState.PATH_PLANNED
    assert result.goal_point is not None
    assert result.path is not None
    assert len(result.path) > 2


def test_navigation_state_machine_failed_when_no_target() -> None:
    grid = np.ones((10, 10), dtype=np.uint8)
    semantic_map = SemanticMap.from_records(
        [
            {"category": "table", "points": [[0.4, 0.5], [0.5, 0.5], [0.6, 0.5]]},
        ]
    )

    sm = NavigationStateMachine(
        semantic_map=semantic_map,
        occupancy_grid=grid,
        meters_per_cell=0.1,
        free_value=1,
        unknown_value=2,
    )
    result = sm.run("go to the chair", robot_xy=(0.1, 0.1))

    assert result.state == NavigationState.FAILED
    assert "No semantic target region" in result.message


def test_scene_export_loader_with_vlmaps_labels(tmp_path: Path) -> None:
    scene_dir = tmp_path / "scene_export"
    scene_dir.mkdir(parents=True)

    occ = np.ones((10, 10), dtype=np.uint8)  # 1=free
    occ[5, 5] = 0  # obstacle
    np.save(scene_dir / "occupancy_map.npy", occ)

    metadata = {
        "scene_name": "library_scene_01",
        "map_height": 10,
        "map_width": 10,
        "cell_size_m": 0.5,
        "origin_world": [0.0, 0.0, 0.0],
        "grid_to_world": {"row_axis": "z", "col_axis": "x"},
        "occupancy_label_def": {"0": "obstacle", "1": "free", "2": "unknown"},
    }
    (scene_dir / "map_metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    semantic_objects = {
        "objects": [
            {
                "object_id": 0,
                "label": "chair",
                "score": 0.91,
                "grid_centroid": [2, 3],
                "grid_pixels": [[2, 3], [2, 4], [3, 3]],
            }
        ]
    }
    (scene_dir / "semantic_objects.json").write_text(json.dumps(semantic_objects), encoding="utf-8")

    bundle = load_scene_export(str(scene_dir))
    free_value, unknown_value = infer_occupancy_labels(bundle.metadata)

    assert bundle.occupancy_map.shape == (10, 10)
    assert free_value == 1
    assert unknown_value == 2

    sm = NavigationStateMachine(
        semantic_map=bundle.semantic_map,
        occupancy_grid=bundle.occupancy_map,
        meters_per_cell=bundle.metadata.cell_size_m,
        free_value=free_value,
        unknown_value=unknown_value,
    )
    result = sm.run("go to the chair", robot_xy=(0.0, 0.0))
    assert result.state in (NavigationState.PATH_PLANNED, NavigationState.ARRIVED)


def test_vlfm_integration_compatibility_layer() -> None:
    mod = importlib.import_module("vlfm.integration")
    parser = mod.LanguageParser()
    parsed = parser.parse("go to the desk")
    assert parsed.target_object == "desk"
