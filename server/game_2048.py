"""
Core 2048 game logic.

A 4x4 sliding tile puzzle where tiles with the same number merge
when moved in one of four directions. The goal is to create a tile
with the value 2048.
"""

import random
from enum import IntEnum
from typing import List, Optional, Tuple


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Game2048:
    """Pure game logic for 2048."""

    def __init__(self, size: int = 4, seed: Optional[int] = None):
        self.size = size
        self.rng = random.Random(seed)
        self.board: List[List[int]] = []
        self.score: int = 0
        self.done: bool = False
        self.won: bool = False
        self.reset()

    def reset(self, seed: Optional[int] = None) -> None:
        if seed is not None:
            self.rng = random.Random(seed)
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.done = False
        self.won = False
        self._spawn_tile()
        self._spawn_tile()

    def _spawn_tile(self) -> None:
        empty = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]
        if not empty:
            return
        r, c = self.rng.choice(empty)
        self.board[r][c] = 4 if self.rng.random() < 0.1 else 2

    def _compress(self, row: List[int]) -> Tuple[List[int], int]:
        """Slide and merge a single row to the left. Returns (new_row, merge_score)."""
        # Remove zeros
        filtered = [x for x in row if x != 0]
        merged = []
        merge_score = 0
        skip = False
        for i in range(len(filtered)):
            if skip:
                skip = False
                continue
            if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
                val = filtered[i] * 2
                merged.append(val)
                merge_score += val
                skip = True
            else:
                merged.append(filtered[i])
        # Pad with zeros
        merged.extend([0] * (self.size - len(merged)))
        return merged, merge_score

    def _move(self, direction: Direction) -> int:
        """Apply a move and return the score gained. Does not spawn new tile."""
        merge_score = 0

        if direction == Direction.LEFT:
            for r in range(self.size):
                self.board[r], s = self._compress(self.board[r])
                merge_score += s

        elif direction == Direction.RIGHT:
            for r in range(self.size):
                row_reversed = self.board[r][::-1]
                compressed, s = self._compress(row_reversed)
                self.board[r] = compressed[::-1]
                merge_score += s

        elif direction == Direction.UP:
            for c in range(self.size):
                col = [self.board[r][c] for r in range(self.size)]
                compressed, s = self._compress(col)
                for r in range(self.size):
                    self.board[r][c] = compressed[r]
                merge_score += s

        elif direction == Direction.DOWN:
            for c in range(self.size):
                col = [self.board[r][c] for r in range(self.size)][::-1]
                compressed, s = self._compress(col)
                compressed = compressed[::-1]
                for r in range(self.size):
                    self.board[r][c] = compressed[r]
                merge_score += s

        return merge_score

    def _board_copy(self) -> List[List[int]]:
        return [row[:] for row in self.board]

    def can_move(self, direction: Direction) -> bool:
        """Check if a move in the given direction would change the board."""
        old = self._board_copy()
        self._move(direction)
        changed = self.board != old
        self.board = old
        return changed

    def legal_actions(self) -> List[int]:
        return [d.value for d in Direction if self.can_move(d)]

    def step(self, direction: int) -> Tuple[int, bool]:
        """
        Execute a move. Returns (score_gained, done).
        """
        d = Direction(direction)
        if not self.can_move(d):
            return 0, self.done

        merge_score = self._move(d)
        self.score += merge_score
        self._spawn_tile()

        # Check win
        for row in self.board:
            if 2048 in row:
                self.won = True

        # Check game over
        if not self.legal_actions():
            self.done = True

        return merge_score, self.done

    def max_tile(self) -> int:
        return max(max(row) for row in self.board)

    def render(self) -> str:
        """Text render of the board."""
        lines = []
        for row in self.board:
            lines.append(" | ".join(f"{v:>4}" if v else "   ." for v in row))
        return "\n".join(lines)
