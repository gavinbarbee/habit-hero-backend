from __future__ import annotations

from dataclasses import dataclass

from habit_hero.application.ports import HabitRepository
from habit_hero.domain.entities import Habit


@dataclass
class ListHabitsRequest:
    """
    Request object for listing habits for a user.
    """
    user_id: str


class ListHabitsUseCase:
    """
    Simple use case to return all active habits for a user.
    """

    def __init__(self, habits: HabitRepository) -> None:
        self.habits = habits

    def execute(self, req: ListHabitsRequest) -> list[Habit]:
        return self.habits.list_for_user(req.user_id)
