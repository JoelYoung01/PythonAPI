from typing import Union
from pydantic import BaseModel

from fastapi_utils.api_model import APIModel


class FaqCreate(APIModel):
    """The payload required to Create a new Faq"""

    question: str
    asker: str | None = None

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "question": "Now what if they ask a good question?",
                    "asker": "Steve",
                },
            ]
        }


class FaqUpdate(APIModel):
    """The payload required to Update an existing Faq"""

    question: str | None = None
    asker: str | None = None
    answer: str | None = None
    answerer: str | None = None


class Faq(APIModel):
    """The payload returned when a Faq is retrieved"""

    id: int
    question: str
    asker: str | None
    answer: str | None
    answerer: str | None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 24,
                    "question": "This is a very good question, please answer?",
                    "answer": "This is a very good answer, please ask more questions",
                    "asker": "Steve",
                    "answerer": "Alex",
                },
                {
                    "id": 13,
                    "question": "This is a very good question with no answer?",
                    "answer": None,
                    "asker": "Steve",
                    "answerer": None,
                },
            ]
        }
