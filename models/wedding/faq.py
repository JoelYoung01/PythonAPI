from pydantic import BaseModel


class Faq(BaseModel):
    id: int
    question: str
    answer: str
    asker_id: int
    answerer_id: int

    model_config = {
        "json_schema_extra": {
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
    }
