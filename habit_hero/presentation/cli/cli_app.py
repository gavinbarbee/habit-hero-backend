from __future__ import annotations

from datetime import datetime, date

from habit_hero.domain.entities import User, Character
from habit_hero.application.use_cases.complete_habit import (
    CompleteHabitUseCase,
    CompleteHabitRequest,
)
from habit_hero.application.use_cases.create_habit import (
    CreateHabitUseCase,
    CreateHabitRequest,
)
from habit_hero.application.use_cases.list_habits import (
    ListHabitsUseCase,
    ListHabitsRequest,
)
from habit_hero.infrastructure.persistence.in_memory_repositories import (
    InMemoryUserRepository,
    InMemoryCharacterRepository,
    InMemoryHabitRepository,
    InMemoryHabitLogRepository,
    InMemoryStreakRepository,
)




def run_demo() -> None:
    """
    Very simple demo that:
      1) Creates a user, character, and one habit
      2) Runs CompleteHabitUseCase once
      3) Prints the updated level, XP, and streak
    """

    # 1. Set up in-memory "database" (repos)
    user_repo = InMemoryUserRepository()
    character_repo = InMemoryCharacterRepository()
    habit_repo = InMemoryHabitRepository()
    log_repo = InMemoryHabitLogRepository()
    streak_repo = InMemoryStreakRepository()

    # 2. Create a user and save it
    user = User(
        id="user-1",
        long_term_vision="Become the strongest, clearest version of myself.",
        created_at=datetime.utcnow(),
    )
    user_repo.save(user)

    # 3. Create a character for that user
    character = Character(user_id=user.id)
    character_repo.save(character)

    # 4. Create one habit via the use case
    create_habit = CreateHabitUseCase(habits=habit_repo)
    habit = create_habit.execute(
        CreateHabitRequest(
            user_id=user.id,
            name="Morning training",
            cue="After I wake up",
            action="Lift weights for 45 minutes",
            reward="Feel strong and clear for the day",
            estimated_minutes=45,
            base_xp=10,
        )
    )

    # 5. Wire up the use case
    complete_habit = CompleteHabitUseCase(
        habits=habit_repo,
        logs=log_repo,
        streaks=streak_repo,
        characters=character_repo,
    )
    list_habits = ListHabitsUseCase(habits=habit_repo)

    # 6. Execute the use case once (simulate completing the habit today)
    today = date.today()
    request = CompleteHabitRequest(
        user_id=user.id,
        habit_id=habit.id,
        day=today,
    )
    complete_habit.execute(request)

    # 7. List all habits for this user
    habit_list = list_habits.execute(
        ListHabitsRequest(user_id=user.id)
    )

    # 8. Read back the updated state
    updated_character = character_repo.get_for_user(user.id)
    streak = streak_repo.get(user.id, habit.id)

    # 9. Print results to the console
    print("=== Habit Hero Demo: Complete Habit Once ===")
    print(f"User: {user.id}")
    print(f"Habit: {habit.name}")

    if updated_character:
        print(
            f"Character Level: {updated_character.level} | "
            f"XP: {updated_character.xp}/{updated_character.xp_to_next_level}"
        )

    if streak:
        print(
            f"Current streak: {streak.current_streak} day(s) | "
            f"Longest streak: {streak.longest_streak} day(s)"
        )

    print("\nAll habits for this user:")
    for h in habit_list:
        print(f"- {h.name} (XP: {h.base_xp}, Active: {h.active})")
