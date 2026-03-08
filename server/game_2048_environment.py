"""
2048 Game Environment Implementation.

An OpenEnv environment wrapping the classic 2048 sliding tile puzzle.
The agent chooses one of four directions (up/down/left/right) each step.
Reward is the score gained from tile merges on that step.
"""

from typing import Any, Optional
from uuid import uuid4

# Support both in-repo and standalone imports
try:
    from openenv.core.env_server.interfaces import Environment
    from openenv.core.env_server.types import State

    from ..models import Game2048Action, Game2048Observation, Game2048State
except ImportError:
    from openenv_core.env_server.interfaces import Environment
    from openenv_core.env_server.types import State

    from models import Game2048Action, Game2048Observation, Game2048State

from .game_2048 import Game2048


class Game2048Environment(Environment[Game2048Action, Game2048Observation, Game2048State]):
    """
    OpenEnv environment for the 2048 game.

    The agent slides tiles in one of four directions. Equal tiles merge,
    doubling their value and adding to the score. A new tile (2 or 4)
    spawns after each valid move. The episode ends when no moves remain.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self, seed: Optional[int] = None):
        self.game = Game2048(seed=seed)
        self._state = Game2048State(episode_id=str(uuid4()), step_count=0)
        self._sync_state()

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Game2048Observation:
        self.game.reset(seed=seed)
        self._state = Game2048State(
            episode_id=episode_id or str(uuid4()),
            step_count=0,
        )
        self._sync_state()
        return self._build_observation(reward=0.0)

    def step(
        self,
        action: Game2048Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Game2048Observation:
        self._state.step_count += 1
        merge_score, done = self.game.step(action.action)
        self._sync_state()
        return self._build_observation(reward=float(merge_score))

    def _build_observation(self, reward: float) -> Game2048Observation:
        return Game2048Observation(
            board=[row[:] for row in self.game.board],
            score=self.game.score,
            legal_actions=self.game.legal_actions(),
            max_tile=self.game.max_tile(),
            board_text=self.game.render(),
            reward=reward,
            done=self.game.done,
            metadata={
                "won": self.game.won,
                "step": self._state.step_count,
            },
        )

    def _sync_state(self) -> None:
        self._state.done = self.game.done
        self._state.won = self.game.won
        self._state.score = self.game.score
        self._state.max_tile = self.game.max_tile()

    @property
    def state(self) -> State:
        return self._state
