from typing import Tuple

import numpy as np

from .semantic_map import SemanticRegion


class GoalSelectionError(RuntimeError):
    pass


class GoalSelector:
    """Converts semantic regions into a reachable 2D navigation goal."""

    def __init__(self, occupancy_grid: np.ndarray, meters_per_cell: float = 0.1) -> None:
        if occupancy_grid.ndim != 2:
            raise ValueError("occupancy_grid must be a 2D array.")
        self._grid = occupancy_grid
        self._m_per_cell = meters_per_cell

    def select_goal(self, region: SemanticRegion, max_radius_cells: int = 10) -> Tuple[float, float]:
        center = region.centroid
        center_cell = self._xy_to_cell(center)

        for radius in range(max_radius_cells + 1):
            cells = self._ring_cells(center_cell, radius)
            for row, col in cells:
                if self._is_free(row, col):
                    return self._cell_to_xy((row, col))

        raise GoalSelectionError(
            f"No reachable free-space goal found near semantic target '{region.category}'."
        )

    def _is_free(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= self._grid.shape[0] or col >= self._grid.shape[1]:
            return False
        return int(self._grid[row, col]) == 0

    @staticmethod
    def _ring_cells(center: Tuple[int, int], radius: int) -> Tuple[Tuple[int, int], ...]:
        r0, c0 = center
        if radius == 0:
            return ((r0, c0),)
        cells = []
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                if max(abs(dr), abs(dc)) == radius:
                    cells.append((r0 + dr, c0 + dc))
        return tuple(cells)

    def _xy_to_cell(self, xy: np.ndarray) -> Tuple[int, int]:
        col = int(round(xy[0] / self._m_per_cell))
        row = int(round(xy[1] / self._m_per_cell))
        return row, col

    def _cell_to_xy(self, cell: Tuple[int, int]) -> Tuple[float, float]:
        row, col = cell
        return (col * self._m_per_cell, row * self._m_per_cell)
