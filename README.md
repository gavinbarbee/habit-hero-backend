# Habit Hero — Backend (Version 0)

This repository contains the backend foundation for **Habit Hero**, an early-stage habit and identity-building application.

**Version 0 goal:** ship a minimal, working backend that demonstrates the core loop:  
**create user → create habit → complete habit → receive XP/streak feedback → log LifeForce → see progression**.

This version prioritizes clarity and correctness over polish, scale, or completeness.

---

## What this project is

- A **Python backend** built using **clean architecture principles**
- Focused on **domain logic**, **use cases**, and **testability**
- Designed as a foundation that can later support:
  - an API (e.g., FastAPI)
  - a database (e.g., SQLite/Postgres)
  - AI-assisted onboarding (server-side, no keys in clients)
  - a frontend or mobile app

This repository is public as a learning artifact and an evolving system.

---

## Core features implemented (Version 0)

### Architecture
- `domain` — core entities and business rules  
- `application` — use cases + ports (interfaces)  
- `infrastructure` — in-memory persistence implementations  
- `presentation` — a simple CLI demo  

### Domain models
- **User**
- **Character** (XP + level progression)
- **Habit**
- **Streak tracking**
- **Habit logs**
- **LifeForce** (daily exercise + diet alignment)

### Use cases
- Create user (automatically creates a character)
- Create habit
- Complete habit (XP + streak updates + log entry)
- List habits for a user
- Log LifeForce (exercise + diet) and award XP

### Testing
- Unit tests covering:
  - streak logic
  - XP calculation
  - character leveling
  - LifeForce logging

---

## Quick start

### 1) Install dependencies
```bash
pip install -r requirements.txt
