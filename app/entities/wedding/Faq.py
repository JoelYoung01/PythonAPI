from pydantic import BaseModel


class FaqBase(BaseModel):
    question: str
    asker_id: int | None

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "id": 24,
                    "question": "This is a very good question, please answer?",
                    "asker_id": 2,
                },
            ]
        }


class FaqAnswer(BaseModel):
    id: int
    answer: str
    answerer_id: int


class FaqCreate(FaqBase):
    pass


class Faq(FaqBase):
    id: int
    answer: str
    answerer_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 24,
                    "question": "This is a very good question, please answer?",
                    "answer": "This is a very good answer, please ask more questions",
                    "asker_id": 2,
                    "answerer_id": 7,
                },
                {
                    "id": 13,
                    "question": "This is a very good question with no answer?",
                    "answer": None,
                    "asker_id": 7,
                    "answerer_id": None,
                },
            ]
        }
