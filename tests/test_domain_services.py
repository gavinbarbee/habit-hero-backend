from pathlib import Path
import sys

# Ensure the project root (where habit_hero/ lives) is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from datetime import date

from habit_hero.domain.entities import Habit, StreakState, Character
from habit_hero.domain.services import (
    calculate_new_streak,
    xp_gain_for_habit,
    apply_xp,
)

def make_sample_habit() -> Habit:
    return Habit(
        id="habit-1",
        user_id="user-1",
        name="Morning training",
        cue="After I wake up",
        action="Lift weights for 45 minutes",
        reward="Feel strong and clear for the day",
        estimated_minutes=45,
        base_xp=10,
        is_bad_habit=False,
        replaces_habit_id=None,
        active=True,
    )


def test_calculate_new_streak_starts_at_one_when_no_previous():
    habit = make_sample_habit()
    today = date(2025, 1, 1)

    new_streak = calculate_new_streak(
        existing=None,
        habit=habit,
        today=today,
    )

    assert new_streak.current_streak == 1
    assert new_streak.longest_streak == 1
    assert new_streak.last_completed_day == today


def test_calculate_new_streak_increments_when_consecutive_day():
    habit = make_sample_habit()
    yesterday = date(2025, 1, 1)
    today = date(2025, 1, 2)

    existing = StreakState(
        user_id="user-1",
        habit_id="habit-1",
        current_streak=3,
        longest_streak=5,
        last_completed_day=yesterday,
    )

    new_streak = calculate_new_streak(
        existing=existing,
        habit=habit,
        today=today,
    )

    assert new_streak.current_streak == 4
    # longest_streak should stay at 5 since 4 < 5
    assert new_streak.longest_streak == 5
    assert new_streak.last_completed_day == today


def test_calculate_new_streak_resets_when_gap():
    habit = make_sample_habit()
    last = date(2025, 1, 1)
    today = date(2025, 1, 5)  # big gap

    existing = StreakState(
        user_id="user-1",
        habit_id="habit-1",
        current_streak=3,
        longest_streak=5,
        last_completed_day=last,
    )

    new_streak = calculate_new_streak(
        existing=existing,
        habit=habit,
        today=today,
    )

    assert new_streak.current_streak == 1
    # longest should still keep the max historical streak
    assert new_streak.longest_streak == 5
    assert new_streak.last_completed_day == today


def test_xp_gain_for_habit_increases_with_streak():
    habit = make_sample_habit()

    streak_1 = StreakState(
        user_id="user-1",
        habit_id="habit-1",
        current_streak=1,
        longest_streak=1,
        last_completed_day=date(2025, 1, 1),
    )
    streak_5 = StreakState(
        user_id="user-1",
        habit_id="habit-1",
        current_streak=5,
        longest_streak=5,
        last_completed_day=date(2025, 1, 5),
    )

    xp_1 = xp_gain_for_habit(habit, streak_1)
    xp_5 = xp_gain_for_habit(habit, streak_5)

    assert xp_1 >= habit.base_xp
    assert xp_5 >= xp_1  # higher streak should not give less XP


def test_apply_xp_levels_up_character():
    character = Character(user_id="user-1")
    # assume xp_to_next_level starts at 100 in your implementation
    gained = 150

    updated = apply_xp(character, gained)

    # should have at least leveled up once
    assert updated.level >= 2
    assert updated.xp >= 0
    # total xp should be >= gained (but distributed across levels)
    # we can't hard-code exact values without your exact XP curve,
    # but we can assert that xp_to_next_level is positive.
    assert updated.xp_to_next_level > 0
