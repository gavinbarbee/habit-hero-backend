from __future__ import annotations

from datetime import date
from typing import Dict, Optional

from habit_hero.domain.entities import (
    User,
    Character,
    Habit,
    HabitLog,
    StreakState,
    LifeForceCheck,
)
from habit_hero.application.ports import (
    UserRepository,
    CharacterRepository,
    HabitRepository,
    HabitLogRepository,
    StreakRepository,
    LifeForceRepository,
)


class InMemoryUserRepository(UserRepository):
    """
    Stores user data in memory only.
    This is perfect for early development and tests.
    Nothing is saved to disk.
    """

    def __init__(self) -> None:
        self._users: Dict[str, User] = {}

    def get(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def save(self, user: User) -> None:
        self._users[user.id] = user
from habit_hero.application.ports import (
    UserRepository,
    CharacterRepository,
    HabitRepository,
    HabitLogRepository,
    StreakRepository,
)

class InMemoryCharacterRepository(CharacterRepository):
    """
    In-memory storage for Character objects.
    One character per user (for now).
    """

    def __init__(self) -> None:
        self._characters: Dict[str, Character] = {}  # key: user_id

    def get_for_user(self, user_id: str) -> Optional[Character]:
        return self._characters.get(user_id)

    def save(self, character: Character) -> None:
        self._characters[character.user_id] = character

class InMemoryHabitRepository(HabitRepository):
    """
    In-memory storage for Habit objects.
    Supports:
      - get by id
      - list all habits for a user
      - save / update a habit
    """

    def __init__(self) -> None:
        self._habits: Dict[str, Habit] = {}  # key: habit_id

    def get(self, habit_id: str) -> Optional[Habit]:
        return self._habits.get(habit_id)

    def list_for_user(self, user_id: str) -> list[Habit]:
        return [
            habit
            for habit in self._habits.values()
            if habit.user_id == user_id and habit.active
        ]

    def save(self, habit: Habit) -> None:
        self._habits[habit.id] = habit

class InMemoryHabitLogRepository(HabitLogRepository):
    """
    In-memory storage for habit completion logs.
    """

    def __init__(self) -> None:
        self._logs: Dict[str, HabitLog] = {}  # key: log_id

    def list_for_day(self, user_id: str, day: date) -> list[HabitLog]:
        return [
            log
            for log in self._logs.values()
            if log.user_id == user_id and log.day == day
        ]

    def save(self, log: HabitLog) -> None:
        self._logs[log.id] = log

class InMemoryStreakRepository(StreakRepository):
    """
    In-memory storage for streak state per (user, habit).
    """

    def __init__(self) -> None:
        # key: (user_id, habit_id) as a single string "user|habit"
        self._streaks: Dict[str, StreakState] = {}

    def _key(self, user_id: str, habit_id: str) -> str:
        return f"{user_id}|{habit_id}"

    def get(self, user_id: str, habit_id: str) -> Optional[StreakState]:
        return self._streaks.get(self._key(user_id, habit_id))

    def save(self, streak: StreakState) -> None:
        key = self._key(streak.user_id, streak.habit_id)
        self._streaks[key] = streak
class InMemoryLifeForceRepository(LifeForceRepository):
    def __init__(self) -> None:
        # key: (user_id, day)
        self._storage: Dict[tuple[str, date], LifeForceCheck] = {}

    def save(self, check: LifeForceCheck) -> None:
        key = (check.user_id, check.day)
        self._storage[key] = check

    def get_for_day(self, user_id: str, day: date) -> Optional[LifeForceCheck]:
        return self._storage.get((user_id, day))

