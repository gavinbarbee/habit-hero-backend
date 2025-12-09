from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from habit_hero.application.ports import HabitRepository
from habit_hero.domain.entities import Habit


@dataclass
class CreateHabitRequest:
    """
    Data needed to create a new habit for a user.
    """
    user_id: str
    name: str
    cue: str
    action: str
    reward: str
    estimated_minutes: int
    base_xp: int | None = None
    is_bad_habit: bool = False
    replaces_habit_id: str | None = None


class CreateHabitUseCase:
    """
    Use case to create a new habit and store it via the HabitRepository.
    """

    def __init__(self, habits: HabitRepository) -> None:
        self.habits = habits

    def execute(self, req: CreateHabitRequest) -> Habit:
        # Decide base XP if not explicitly set
        if req.base_xp is not None:
            base_xp = req.base_xp
        else:
            # Very simple rule: 5 XP per 10 minutes, capped between 5 and 50
            base_xp = max(5, min(50, (req.estimated_minutes // 10) * 5))

        habit = Habit(
            id=f"habit-{uuid4().hex}",
            user_id=req.user_id,
            name=req.name,
            cue=req.cue,
            action=req.action,
            reward=req.reward,
            estimated_minutes=req.estimated_minutes,
            base_xp=base_xp,
            is_bad_habit=req.is_bad_habit,
            replaces_habit_id=req.replaces_habit_id,
            active=True,
        )

        self.habits.save(habit)
        return habit
