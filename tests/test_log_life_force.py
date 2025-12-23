from pathlib import Path
import sys

# Ensure the project root (where habit_hero/ lives) is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from datetime import date

from habit_hero.domain.entities import Character
from habit_hero.infrastructure.persistence.in_memory_repositories import (
    InMemoryLifeForceRepository,
    InMemoryCharacterRepository,
)
from habit_hero.application.use_cases.log_life_force import (
    LogLifeForceUseCase,
    LogLifeForceRequest,
)


def test_log_life_force_saves_check_and_awards_xp():
    # Arrange: in-memory repos and a character
    lf_repo = InMemoryLifeForceRepository()
    character_repo = InMemoryCharacterRepository()

    # Create a starting character for the user
    user_id = "user-1"
    starting_character = Character(user_id=user_id)
    character_repo.save(starting_character)

    use_case = LogLifeForceUseCase(
        life_force=lf_repo,
        characters=character_repo,
    )

    # Act: log a strong LifeForce day
    req = LogLifeForceRequest(
        user_id=user_id,
        day=date(2025, 1, 1),
        exercise_score=3,
        diet_score=3,
    )
    result = use_case.execute(req)

    # Assert: LifeForceCheck is saved
    saved = lf_repo.get_for_day(user_id, req.day)
    assert saved is not None
    assert saved.exercise_score == 3
    assert saved.diet_score == 3

    # XP should be > 0 for a good day
    assert result.xp_awarded > 0

    # Character should be updated
    assert result.character is not None
    assert result.character.level >= 1
    # character should have gained XP
    assert result.character.xp > 0


def test_log_life_force_clamps_scores_and_handles_zero_alignment():
    lf_repo = InMemoryLifeForceRepository()
    character_repo = InMemoryCharacterRepository()

    user_id = "user-2"
    starting_character = Character(user_id=user_id)
    character_repo.save(starting_character)

    use_case = LogLifeForceUseCase(
        life_force=lf_repo,
        characters=character_repo,
    )

    # Scores below 0 and above 3 should be clamped
    req = LogLifeForceRequest(
        user_id=user_id,
        day=date(2025, 1, 2),
        exercise_score=-5,
        diet_score=10,
    )
    result = use_case.execute(req)

    saved = lf_repo.get_for_day(user_id, req.day)
    assert saved is not None
    # Expect clamped to 0 and 3
    assert saved.exercise_score == 0
    assert saved.diet_score == 3

    # XP should be based on clamped values: (0 + 3) * 5 = 15
    assert result.xp_awarded == 15
