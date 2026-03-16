import heapq
from typing import Dict, List, Optional, Tuple

import numpy as np


class PlanningError(RuntimeError):
    pass


class AStarPlanner:
    """Simple 2D grid A* planner.

    Occupancy convention:
    - 0: free
    - 1: obstacle
    - 2: unknown (treated as blocked by default)
    """

    def __init__(self, occupancy_grid: np.ndarray, meters_per_cell: float = 0.1, allow_unknown: bool = False) -> None:
        if occupancy_grid.ndim != 2:
            raise ValueError("occupancy_grid must be 2D.")
        self._grid = occupancy_grid
        self._m_per_cell = meters_per_cell
        self._allow_unknown = allow_unknown

    def plan(self, start_xy: Tuple[float, float], goal_xy: Tuple[float, float]) -> List[Tuple[float, float]]:
        start = self._xy_to_cell(start_xy)
        goal = self._xy_to_cell(goal_xy)
        if not self._is_walkable(goal):
            raise PlanningError("Goal is not in walkable space.")
        if not self._is_walkable(start):
            raise PlanningError("Start is not in walkable space.")

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}
        open_heap: List[Tuple[float, Tuple[int, int]]] = []
        heapq.heappush(open_heap, (self._heuristic(start, goal), start))
        visited = set()

        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                return [self._cell_to_xy(c) for c in self._reconstruct_path(came_from, current)]

            for nxt in self._neighbors(current):
                tentative = g_score[current] + self._step_cost(current, nxt)
                if tentative < g_score.get(nxt, float("inf")):
                    came_from[nxt] = current
                    g_score[nxt] = tentative
                    f_score = tentative + self._heuristic(nxt, goal)
                    heapq.heappush(open_heap, (f_score, nxt))

        raise PlanningError("A* failed to find a path.")

    def _neighbors(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        r, c = cell
        candidates = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
            (r - 1, c - 1),
            (r - 1, c + 1),
            (r + 1, c - 1),
            (r + 1, c + 1),
        ]
        return [x for x in candidates if self._is_walkable(x)]

    def _is_walkable(self, cell: Tuple[int, int]) -> bool:
        r, c = cell
        if r < 0 or c < 0 or r >= self._grid.shape[0] or c >= self._grid.shape[1]:
            return False
        value = int(self._grid[r, c])
        if value == 0:
            return True
        if value == 2:
            return self._allow_unknown
        return False

    @staticmethod
    def _heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return float(np.hypot(a[0] - b[0], a[1] - b[1]))

    @staticmethod
    def _step_cost(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        dr = abs(a[0] - b[0])
        dc = abs(a[1] - b[1])
        return 1.41421356 if dr == 1 and dc == 1 else 1.0

    @staticmethod
    def _reconstruct_path(
        came_from: Dict[Tuple[int, int], Tuple[int, int]],
        current: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def _xy_to_cell(self, xy: Tuple[float, float]) -> Tuple[int, int]:
        col = int(round(xy[0] / self._m_per_cell))
        row = int(round(xy[1] / self._m_per_cell))
        return row, col

    def _cell_to_xy(self, cell: Tuple[int, int]) -> Tuple[float, float]:
        row, col = cell
        return (col * self._m_per_cell, row * self._m_per_cell)
