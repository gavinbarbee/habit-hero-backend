from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from habit_hero.application.ports import (
    HabitRepository,
    HabitLogRepository,
    StreakRepository,
    CharacterRepository,
)
from habit_hero.domain.entities import HabitLog
from habit_hero.domain.services import (
    calculate_new_streak,
    xp_gain_for_habit,
    apply_xp,
)


@dataclass
class CompleteHabitRequest:
    """
    Data needed to complete a habit for a given user on a given day.
    """
    user_id: str
    habit_id: str
    day: date


class CompleteHabitUseCase:
    """
    Orchestrates what happens when a user completes a habit:
      1) fetch the habit
      2) fetch existing streak
      3) calculate new streak
      4) calculate XP
      5) create a HabitLog
      6) update the character's XP / level
      7) save everything
    """

    def __init__(
        self,
        habits: HabitRepository,
        logs: HabitLogRepository,
        streaks: StreakRepository,
        characters: CharacterRepository,
    ) -> None:
        self.habits = habits
        self.logs = logs
        self.streaks = streaks
        self.characters = characters

    def execute(self, req: CompleteHabitRequest) -> None:
        """
        Perform the full 'complete habit' flow for the given request.
        """
        # 1. Fetch the habit
        habit = self.habits.get(req.habit_id)
        if habit is None or habit.user_id != req.user_id:
            raise ValueError("Habit not found for this user.")

        # 2. Fetch existing streak
        existing_streak = self.streaks.get(req.user_id, req.habit_id)

        # 3. Calculate new streak
        new_streak = calculate_new_streak(existing_streak, habit, req.day)

        # 4. Calculate XP
        xp = xp_gain_for_habit(habit, new_streak)

        # 5. Create log
        log = HabitLog(
            id=f"log-{req.habit_id}-{req.day.isoformat()}",
            user_id=req.user_id,
            habit_id=req.habit_id,
            day=req.day,
            completed_at=datetime.utcnow(),
            xp_earned=xp,
        )

        # 6. Update character
        character = self.characters.get_for_user(req.user_id)
        if character is not None:
            updated = apply_xp(character, xp)
            self.characters.save(updated)

        # 7. Save streak + log
        self.streaks.save(new_streak)
        self.logs.save(log)

        return None
