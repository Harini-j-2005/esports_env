# 🎮 Esports Ops Environment (OpenEnv RL Benchmark)

## 📌 Overview

This project presents a reinforcement learning environment that simulates real-world decision-making for professional esports players. The environment models how training, performance analysis, and fan engagement strategies impact a player's skill, fatigue, and confidence over time.

The goal is to enable AI agents to learn optimal decision-making strategies through structured interaction and reward-based feedback.

---

## 🎯 Motivation

Professional esports players must continuously balance:
- Skill improvement through targeted training
- Performance optimization via match analysis
- Fan engagement and public presence

This environment captures these workflows and provides a standardized benchmark for evaluating AI agents in esports operations.

---

## 🧠 Environment Design

The environment follows the OpenEnv specification with:
- Typed observation, action, and reward models (Pydantic)
- Step-based interaction (`step`, `reset`, `state`)
- Deterministic task grading (0.0–1.0 scoring)

---

## 🧩 Tasks

### 1. Training Optimization (Easy)
**Objective:** Improve the weakest player skill (aim, reaction, strategy)

**Impact:**
- Increases skill metrics
- Increases fatigue

---

### 2. Performance Analysis (Medium)
**Objective:** Identify performance issues and improve player condition

**Impact:**
- Reduces fatigue
- Increases confidence

---

### 3. Fan Engagement (Hard)
**Objective:** Respond appropriately to fan interactions

**Impact:**
- Increases player confidence (fan trust proxy)
- Penalizes poor engagement behavior

---


## 👁️ Observation Space

```json
{
  "player": {
    "aim": int,
    "reaction": int,
    "strategy": int,
    "fatigue": int,
    "confidence": int
  }
}