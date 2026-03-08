---
title: Game 2048 Env
emoji: 🎮
colorFrom: yellow
colorTo: red
sdk: docker
app_port: 7860
tags:
  - openenv
  - reinforcement-learning
  - "2048"
  - game
---

# 2048 Game Environment for OpenEnv

A classic 2048 sliding tile puzzle environment for agentic RL training, built on the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework.

## Overview

The agent controls a 4x4 grid where tiles slide and merge. Equal-valued tiles merge on collision, doubling their value. After each move a new tile (2 or 4) spawns. The episode ends when no valid moves remain. The goal is to reach the 2048 tile.

**Actions:** `0`=up, `1`=down, `2`=left, `3`=right

**Reward:** Score gained from tile merges on each step (e.g., merging two 16s yields reward 32)

**Observation:** Board state (4x4 grid), current score, legal actions, max tile, and text rendering

## Quick Start

### Install

```bash
pip install git+https://huggingface.co/spaces/thaihipster/game-2048-env
```

### Use

```python
from game_2048_env import Game2048Env, Game2048Action

env = Game2048Env(base_url="https://thaihipster-game-2048-env.hf.space")
env.connect()

result = env.reset()
print(result.observation.board_text)

# Take a step (0=up, 1=down, 2=left, 3=right)
result = env.step(Game2048Action(action=2))  # move left
print(f"Score: {result.observation.score}, Max tile: {result.observation.max_tile}")

env.close()
```

### Run Locally

```bash
# Clone and install
git clone <this-repo>
cd game_2048_env
pip install -e .

# Start the server
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

## Environment Details

| Property | Value |
|----------|-------|
| Action space | Discrete(4): up, down, left, right |
| Observation | 4x4 int grid + score + legal actions |
| Reward | Merge score per step |
| Episode end | No valid moves remaining |
| Win condition | Creating a 2048 tile |

## For RL Training

This environment is compatible with:
- [torchforge](https://github.com/meta-pytorch/torchforge) (PyTorch agentic RL)
- [TRL](https://huggingface.co/docs/trl/openenv) (Hugging Face)
- [Unsloth](https://unsloth.ai/) (efficient fine-tuning)
- Any framework supporting the OpenEnv API (`reset()`, `step()`, `state()`)
