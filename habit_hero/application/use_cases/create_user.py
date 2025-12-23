from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from habit_hero.application.ports import UserRepository, CharacterRepository
from habit_hero.domain.entities import User, Character


@dataclass
class CreateUserRequest:
    """
    Data needed to create a new user.
    """
    long_term_vision: str


@dataclass
class CreateUserResponse:
    """
    Result of creating a user: the user and their starting character.
    """
    user: User
    character: Character


class CreateUserUseCase:
    """
    Use case to create a new user and an associated starting character.
    """

    def __init__(
        self,
        users: UserRepository,
        characters: CharacterRepository,
    ) -> None:
        self.users = users
        self.characters = characters

    def execute(self, req: CreateUserRequest) -> CreateUserResponse:
        user = User(
            id=f"user-{uuid4().hex}",
            long_term_vision=req.long_term_vision,
            created_at=datetime.utcnow(),
        )
        self.users.save(user)

        character = Character(user_id=user.id)
        self.characters.save(character)

        return CreateUserResponse(user=user, character=character)
