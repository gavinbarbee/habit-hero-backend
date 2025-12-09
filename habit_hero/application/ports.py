from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from habit_hero.domain.entities import (
    User,
    Character,
    Habit,
    HabitLog,
    StreakState,
    FocusSession,
    LifeForceCheck,
)

class UserRepository(ABC):
    @abstractmethod
    def get(self, user_id: str) -> Optional[User]:
        ...

    @abstractmethod
    def save(self, user: User) -> None:
        ...


class CharacterRepository(ABC):
    @abstractmethod
    def get_for_user(self, user_id: str) -> Optional[Character]:
        ...

    @abstractmethod
    def save(self, character: Character) -> None:
        ...


class HabitRepository(ABC):
    @abstractmethod
    def get(self, habit_id: str) -> Optional[Habit]:
        ...

    @abstractmethod
    def list_for_user(self, user_id: str) -> List[Habit]:
        ...

    @abstractmethod
    def save(self, habit: Habit) -> None:
        ...


class HabitLogRepository(ABC):
    @abstractmethod
    def list_for_day(self, user_id: str, day: date) -> List[HabitLog]:
        ...

    @abstractmethod
    def save(self, log: HabitLog) -> None:
        ...


class StreakRepository(ABC):
    @abstractmethod
    def get(self, user_id: str, habit_id: str) -> Optional[StreakState]:
        ...

    @abstractmethod
    def save(self, streak: StreakState) -> None:
        ...


class FocusSessionRepository(ABC):
    @abstractmethod
    def get(self, session_id: str) -> Optional[FocusSession]:
        ...

    @abstractmethod
    def save(self, session: FocusSession) -> None:
        ...


class LifeForceRepository(ABC):
    @abstractmethod
    def get_for_day(self, user_id: str, day: date) -> Optional[LifeForceCheck]:
        ...

    @abstractmethod
    def save(self, check: LifeForceCheck) -> None:
        ...
