from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import uuid4

from habit_hero.application.ports import LifeForceRepository, CharacterRepository
from habit_hero.domain.entities import LifeForceCheck, Character
from habit_hero.domain.services import apply_xp


@dataclass
class LogLifeForceRequest:
    """
    Log a daily Life Force check for a user.

    exercise_score and diet_score are simple 0–3 ratings:
      0 = not at all
      1 = somewhat
      2 = good
      3 = excellent
    """
    user_id: str
    day: date
    exercise_score: int
    diet_score: int


@dataclass
class LogLifeForceResult:
    """
    Result of logging Life Force: the record, how much XP was given,
    and the updated character (if one exists).
    """
    life_force_check: LifeForceCheck
    xp_awarded: int
    character: Character | None


class LogLifeForceUseCase:
    """
    Use case to log Life Force (exercise + diet alignment) and
    reward the user's character with XP accordingly.
    """

    def __init__(
        self,
        life_force: LifeForceRepository,
        characters: CharacterRepository,
    ) -> None:
        self.life_force = life_force
        self.characters = characters

    def execute(self, req: LogLifeForceRequest) -> LogLifeForceResult:
        # Clamp scores between 0 and 3 to avoid bad data
        exercise = max(0, min(3, req.exercise_score))
        diet = max(0, min(3, req.diet_score))

        lf = LifeForceCheck(
            id=f"lf-{uuid4().hex}",
            user_id=req.user_id,
            day=req.day,
            exercise_score=exercise,
            diet_score=diet,
        )
        self.life_force.save(lf)

        total_score = exercise + diet  # 0–6
        xp_awarded = total_score * 5   # simple rule: 5 XP per point of alignment

        updated_character: Character | None = None
        if xp_awarded > 0:
            character = self.characters.get_for_user(req.user_id)
            if character is not None:
                updated_character = apply_xp(character, xp_awarded)
                self.characters.save(updated_character)

        return LogLifeForceResult(
            life_force_check=lf,
            xp_awarded=xp_awarded,
            character=updated_character,
        )
