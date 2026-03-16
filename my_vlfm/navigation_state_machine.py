from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np

from .goal_selector import GoalSelectionError, GoalSelector
from .language_parser import LanguageParser, ParsedInstruction
from .planner import AStarPlanner, PlanningError
from .semantic_map import SemanticMap, SemanticRegion


class NavigationState(str, Enum):
    SEARCHING = "searching"
    GOAL_SELECTED = "goal selected"
    PATH_PLANNED = "path planned"
    ARRIVED = "arrived"
    FAILED = "failed"


@dataclass
class NavigationResult:
    state: NavigationState
    parsed_instruction: Optional[ParsedInstruction] = None
    target_region: Optional[SemanticRegion] = None
    goal_point: Optional[Tuple[float, float]] = None
    path: Optional[List[Tuple[float, float]]] = None
    message: str = ""


class NavigationStateMachine:
    """Orchestrates language parsing, semantic lookup, goal selection and A*."""

    def __init__(self, semantic_map: SemanticMap, occupancy_grid: np.ndarray, meters_per_cell: float = 0.1) -> None:
        self._parser = LanguageParser()
        self._semantic_map = semantic_map
        self._goal_selector = GoalSelector(occupancy_grid, meters_per_cell=meters_per_cell)
        self._planner = AStarPlanner(occupancy_grid, meters_per_cell=meters_per_cell)

    def run(self, instruction: str, robot_xy: Tuple[float, float], arrival_tolerance_m: float = 0.25) -> NavigationResult:
        parsed = self._parser.parse(instruction)

        candidates = self._semantic_map.query_with_relation(
            target_category=parsed.target_object,
            relation=parsed.relation,
            reference_category=parsed.reference_object,
        )
        if not candidates:
            return NavigationResult(
                state=NavigationState.FAILED,
                parsed_instruction=parsed,
                message="No semantic target region matched the instruction.",
            )

        selected = self._semantic_map.nearest_region(candidates, robot_xy)
        if selected is None:
            return NavigationResult(
                state=NavigationState.FAILED,
                parsed_instruction=parsed,
                message="Target selection failed.",
            )

        try:
            goal = self._goal_selector.select_goal(selected)
        except GoalSelectionError as exc:
            return NavigationResult(
                state=NavigationState.FAILED,
                parsed_instruction=parsed,
                target_region=selected,
                message=str(exc),
            )

        try:
            path = self._planner.plan(robot_xy, goal)
        except PlanningError as exc:
            return NavigationResult(
                state=NavigationState.FAILED,
                parsed_instruction=parsed,
                target_region=selected,
                goal_point=goal,
                message=str(exc),
            )

        dist = float(np.linalg.norm(np.asarray(robot_xy) - np.asarray(goal)))
        final_state = NavigationState.ARRIVED if dist <= arrival_tolerance_m else NavigationState.PATH_PLANNED

        return NavigationResult(
            state=final_state,
            parsed_instruction=parsed,
            target_region=selected,
            goal_point=goal,
            path=path,
            message="Path generated successfully." if final_state == NavigationState.PATH_PLANNED else "Already at goal.",
        )
