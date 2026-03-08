"""
Data models for the 2048 Game Environment.

Actions: 0=up, 1=down, 2=left, 3=right
"""

from typing import List, Optional

from pydantic import Field

# Support both in-repo and standalone imports
try:
    from openenv.core.env_server.types import Action, Observation, State
except ImportError:
    from openenv_core.env_server.types import Action, Observation, State


class Game2048Action(Action):
    """Action for the 2048 environment. 0=up, 1=down, 2=left, 3=right."""

    action: int = Field(ge=0, le=3, description="Direction: 0=up, 1=down, 2=left, 3=right")


class Game2048Observation(Observation):
    """Observation from the 2048 environment."""

    board: List[List[int]] = Field(default_factory=list, description="4x4 game board")
    score: int = Field(default=0, description="Current total score")
    legal_actions: List[int] = Field(default_factory=list, description="Valid action indices")
    max_tile: int = Field(default=0, description="Highest tile value on the board")
    board_text: str = Field(default="", description="Text rendering of the board")


class Game2048State(State):
    """State for the 2048 environment."""

    episode_id: Optional[str] = None
    step_count: int = 0
    done: bool = False
    won: bool = False
    score: int = 0
    max_tile: int = 0
