from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, Optional


@dataclass
class User:
    """
    Core user of the Habit Hero app.
    For now we only track an id and their long-term vision.
    """
    id: str
    long_term_vision: str
    created_at: datetime


@dataclass
class Character:
    """
    Visual/avatar representation of the user in the app.
    This will be used for XP, levels, and cosmetics.
    """
    user_id: str
    level: int = 1
    xp: int = 0
    xp_to_next_level: int = 100
    appearance: Dict[str, str] = field(default_factory=dict)
    # example appearance keys:
    #   "hair_style", "hair_color", "eyes", "skin_tone", "body_type",
    #   "clothing", "color_palette", "vibe"


@dataclass
class Habit:
    """
    A single habit with its cue → action → reward structure.
    """
    id: str
    user_id: str
    name: str
    cue: str
    action: str
    reward: str
    estimated_minutes: int
    base_xp: int
    is_bad_habit: bool = False
    replaces_habit_id: str | None = None
    active: bool = True


@dataclass
class HabitLog:
    """
    A record of a habit completed on a specific day.
    This is how we track streaks, XP gained, and daily behavior.
    """
    id: str
    user_id: str
    habit_id: str
    day: date
    completed_at: Optional[datetime]
    xp_earned: int


@dataclass
class StreakState:
    """
    Tracks the current streak and longest streak for each habit.
    """
    habit_id: str
    user_id: str
    current_streak: int
    longest_streak: int
    last_completed_day: Optional[date]


@dataclass
class FocusSession:
    """
    Represents a focus timer session used for deep work.
    XP is granted when a session is successfully completed.
    """
    id: str
    user_id: str
    duration_minutes: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    xp_earned: int = 0


@dataclass
class LifeForceCheck:
    """
    A lightweight daily alignment check for exercise and diet.
    - exercise_score: 0–3 (how well you trained / moved)
    - diet_score: 0–3 (how well you ate that day)
    """
    id: str
    user_id: str
    day: date
    exercise_score: int
    diet_score: int
