from typing import Union
from pydantic import BaseModel


class FaqBase(BaseModel):
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


class FaqAnswer(BaseModel):
    answer: str
    answerer: str | None = None


class FaqCreate(FaqBase):
    pass


class FaqUpdate(BaseModel):
    question: str | None = None
    asker: str | None = None
    answer: str | None = None
    answerer: str | None = None


class Faq(FaqBase):
    id: int
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
