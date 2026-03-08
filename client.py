"""
2048 Game Environment Client.

Connects to a running Game2048Environment server via WebSocket.
"""

from typing import Dict

# Support both in-repo and standalone imports
try:
    from openenv.core.client_types import StepResult
    from openenv.core.env_client import EnvClient
    from openenv.core.env_server.types import State

    from .models import Game2048Action, Game2048Observation, Game2048State
except ImportError:
    from openenv_core.client_types import StepResult
    from openenv_core.env_client import EnvClient
    from openenv_core.env_server.types import State

    from models import Game2048Action, Game2048Observation, Game2048State


class Game2048Env(EnvClient[Game2048Action, Game2048Observation, Game2048State]):
    """
    Client for the 2048 Game Environment.

    Example:
        >>> with Game2048Env(base_url="http://localhost:8000").sync() as env:
        ...     result = env.reset()
        ...     print(result.observation.board_text)
        ...     result = env.step(Game2048Action(action=2))  # move left
        ...     print(result.observation.score)
    """

    def _step_payload(self, action: Game2048Action) -> Dict:
        return {"action": action.action}

    def _parse_result(self, payload: Dict) -> StepResult[Game2048Observation]:
        obs_data = payload.get("observation", {})
        observation = Game2048Observation(
            board=obs_data.get("board", []),
            score=obs_data.get("score", 0),
            legal_actions=obs_data.get("legal_actions", []),
            max_tile=obs_data.get("max_tile", 0),
            board_text=obs_data.get("board_text", ""),
            done=payload.get("done", False),
            reward=payload.get("reward", 0.0),
            metadata=obs_data.get("metadata", {}),
        )
        return StepResult(
            observation=observation,
            reward=payload.get("reward", 0.0),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> Game2048State:
        return Game2048State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            done=payload.get("done", False),
            won=payload.get("won", False),
            score=payload.get("score", 0),
            max_tile=payload.get("max_tile", 0),
        )
