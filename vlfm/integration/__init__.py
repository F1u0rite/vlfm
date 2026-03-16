"""Compatibility layer.

`vlfm.integration` is kept as a thin interface so existing code keeps working,
while implementation now lives in `my_vlfm`.
"""

from my_vlfm import (  # type: ignore
    AStarPlanner,
    GoalSelectionError,
    GoalSelector,
    LanguageParser,
    NavigationResult,
    NavigationState,
    NavigationStateMachine,
    ParsedInstruction,
    PlanningError,
    SemanticMap,
    SemanticRegion,
)

__all__ = [
    "AStarPlanner",
    "GoalSelectionError",
    "GoalSelector",
    "LanguageParser",
    "NavigationResult",
    "NavigationState",
    "NavigationStateMachine",
    "ParsedInstruction",
    "PlanningError",
    "SemanticMap",
    "SemanticRegion",
]
