from enum import Enum

from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator


class EventStatus(str, Enum):
    Open = "Open"
    Closed = "Closed"


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str
    venue: str
    capacity: int
    organizer: str
    status: EventStatus

    @field_validator("title", "venue", "organizer")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Field must not be empty")

        if len(value.strip()) < 3:
            raise ValueError("Field must contain meaningful text")

        return value.strip()

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value: int):
        if value <= 0:
            raise ValueError("Capacity must be greater than 0")

        return value


class Reservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    event_id: int
    student_name: str
    roll_number: str
    email: EmailStr

    @field_validator("student_name", "roll_number")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Field must not be empty")

        if len(value.strip()) < 2:
            raise ValueError("Field must contain meaningful text")

        return value.strip()