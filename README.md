# 🍳 Maze-Run

A model-free Reinforcement Learning solution to the **Cooking Chef Problem**, a custom grid-world MDP built for the Artificial Intelligence exam.

An agent (the Chef) must navigate a maze-like kitchen, pick up a cooking tool (egg beater), and reach a stove (frying pan / oven) to cook eggs — as fast as possible.

---

## 🧠 Problem Overview

The environment is modeled as an **infinite-horizon MDP** `(S, A, P, R, γ)`:

- **States (S):** every cell of the grid, combined with whether the agent currently holds the tool or not.
- **Actions (A):** `up`, `down`, `left`, `right`, `tunnel`, `take`.
- **Transitions (P):** deterministic in the base scenario (Part A); stochastic in the extended scenario (Part B), where each action has a 50% chance of moving in the perpendicular-right direction instead of the intended one.
- **Reward (R):** shaped to encourage the shortest path to picking up the tool and then reaching a stove.
- **Special mechanic — Gates/Tunnel:** two interlinked cells act as a "portal" connecting the two halves of the map, but the agent must actively choose the `tunnel` action to use it.

The grid is split into two symmetric 4×4 blocks (left and right kitchen counters), each containing one tool and one stove, connected only through the tunnel gate.

## 🎯 Objective

Learn an optimal policy that lets the Chef:
1. Navigate the maze avoiding walls,
2. Pick up the required tool (`take` action),
3. Reach a stove and start cooking — ending the episode.

Two separate policies are learned, since the optimal behavior differs before and after the tool is collected:

| Phase | Q-table | Goal |
|---|---|---|
| **Tool phase** | `tool_q_table` | Reach and pick up the egg beater |
| **Cooking phase** | `cook_q_table` | Reach the stove as fast as possible |

## ⚙️ Approach

The solution uses **Q-learning**, a model-free, off-policy Temporal Difference method — chosen because the assignment explicitly requires computing the optimal policy *without* access to the environment's transition model, treating it purely as a black-box "real world" simulator.

Key design choices:
- **ε-greedy exploration** with decaying `epsilon = 1 / (episode + 1)`, balancing exploration and exploitation over training.
- **Two independent Q-tables** instead of a single flattened `(state, has_tool)` table, keeping the two sub-problems (find tool / find stove) cleanly separated and easier to debug/visualize.
- **Reward shaping:**
  - `-1` per step (encourages shortest paths),
  - `-2` for invalid moves (hitting a wall) or a blocked tunnel attempt,
  - `+200` for picking up the tool,
  - `+500` for reaching the stove while holding the tool (episode-ending reward).

## 🗺️ Visualization

The learned policy is rendered directly on the maze grid: each cell shows an arrow for the greedy action (or `T` / `TUNNEL` labels for the special actions), together with the actual walls of the environment (drawn from the `*_forbidden` action lists), making it easy to visually verify that the policy respects the maze structure.

## 📁 Project Structure

```
.
├── env.py        # MDP environment: states, actions, transition & wall logic
├── agent.py       # Q-learning agent: make_step, policy improvement
├── notebook.ipynb  # Training, evaluation and policy visualization
└── README.md
```

## 🚀 Usage
To use the code just open the Jupyter notebook called "notebook.ipynb"

## 📚 Academic Context

This project was developed as part of the **Artificial Intelligence** course, Reinforcement Learning module, covering both the theoretical MDP formalization (states, actions, transition/reward functions, policy counting, stochastic dynamics) and its practical model-free implementation via Q-learning.

---