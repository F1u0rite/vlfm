import importlib

import numpy as np

from my_vlfm import NavigationState, NavigationStateMachine, SemanticMap
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
    # 20x20 grid with one obstacle block
    grid = np.zeros((20, 20), dtype=np.uint8)
    grid[8:12, 8:12] = 1

    semantic_map = SemanticMap.from_records(
        [
            {"category": "chair", "points": [[1.4, 1.4], [1.5, 1.5], [1.6, 1.4]]},
            {"category": "door", "points": [[1.9, 1.4], [2.0, 1.5], [2.1, 1.4]]},
        ]
    )

    sm = NavigationStateMachine(semantic_map=semantic_map, occupancy_grid=grid, meters_per_cell=0.1)
    result = sm.run("go to the chair near the door", robot_xy=(0.2, 0.2))

    assert result.state == NavigationState.PATH_PLANNED
    assert result.goal_point is not None
    assert result.path is not None
    assert len(result.path) > 2


def test_navigation_state_machine_failed_when_no_target() -> None:
    grid = np.zeros((10, 10), dtype=np.uint8)
    semantic_map = SemanticMap.from_records(
        [
            {"category": "table", "points": [[0.4, 0.5], [0.5, 0.5], [0.6, 0.5]]},
        ]
    )

    sm = NavigationStateMachine(semantic_map=semantic_map, occupancy_grid=grid, meters_per_cell=0.1)
    result = sm.run("go to the chair", robot_xy=(0.1, 0.1))

    assert result.state == NavigationState.FAILED
    assert "No semantic target region" in result.message


def test_vlfm_integration_compatibility_layer() -> None:
    mod = importlib.import_module("vlfm.integration")
    parser = mod.LanguageParser()
    parsed = parser.parse("go to the desk")
    assert parsed.target_object == "desk"
