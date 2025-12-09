from __future__ import annotations

from datetime import date
from typing import Optional

from .entities import Habit, StreakState, Character


def calculate_new_streak(
    existing: Optional[StreakState],
    habit: Habit,
    today: date,
) -> StreakState:
    """
    Given the previous streak and a completion today,
    return the updated streak state for this habit.
    """
    # No previous streak: this is day 1
    if existing is None:
        return StreakState(
            habit_id=habit.id,
            user_id=habit.user_id,
            current_streak=1,
            longest_streak=1,
            last_completed_day=today,
        )

    # If last completion was yesterday → continue streak
    if existing.last_completed_day and (today - existing.last_completed_day).days == 1:
        current = existing.current_streak + 1
    else:
        # Missed a day or more → streak resets to 1
        current = 1

    longest = max(existing.longest_streak, current)

    return StreakState(
        habit_id=habit.id,
        user_id=habit.user_id,
        current_streak=current,
        longest_streak=longest,
        last_completed_day=today,
    )


def xp_gain_for_habit(
    habit: Habit,
    streak: StreakState,
) -> int:
    """
    Basic XP calculation for completing a habit.
    For now:
      - Start with habit.base_xp
      - Add a small bonus based on current streak
    This is a placeholder we can replace with your psych model later.
    """
    base = habit.base_xp

    # +10% XP per 5 days of streak, capped at +50%
    streak_bonus_steps = streak.current_streak // 5
    bonus_multiplier = 1.0 + min(streak_bonus_steps * 0.1, 0.5)

    return int(base * bonus_multiplier)


def apply_xp(
    character: Character,
    gained_xp: int,
) -> Character:
    """
    Apply XP to a character, handling level-ups.

    Simple rule:
      - When xp >= xp_to_next_level, level up
      - Each new level requires level * 100 XP
    """
    xp = character.xp + gained_xp
    level = character.level
    xp_to_next = character.xp_to_next_level

    # Handle multiple level-ups if a big XP chunk comes in
    while xp >= xp_to_next:
        xp -= xp_to_next
        level += 1
        xp_to_next = level * 100

    character.xp = xp
    character.level = level
    character.xp_to_next_level = xp_to_next
    return character
