"""
FastAPI application for the 2048 Game Environment.

Usage:
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
"""

# Support both in-repo and standalone imports
try:
    from openenv.core.env_server.http_server import create_app

    from ..models import Game2048Action, Game2048Observation
    from .game_2048_environment import Game2048Environment
except ImportError:
    from openenv_core.env_server.http_server import create_app

    from models import Game2048Action, Game2048Observation
    from server.game_2048_environment import Game2048Environment

app = create_app(
    Game2048Environment,
    Game2048Action,
    Game2048Observation,
    env_name="game_2048_env",
    max_concurrent_envs=1,
)


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
