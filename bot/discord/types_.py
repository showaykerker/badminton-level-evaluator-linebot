import time
import datetime
import dataclasses
from typing import Optional

@dataclasses.dataclass
class User:
    id: str
    username: str
    unfinished_answers_id: Optional[int] = None
    last_interaction_time: Optional[datetime.datetime] = None

@dataclasses.dataclass
class Answers:
    user_id: str
    q1: Optional[str] = None
    q2: Optional[str] = None
    q3: Optional[str] = None
    q4: Optional[str] = None
    q5: Optional[str] = None
    q6: Optional[str] = None
    q7: Optional[str] = None
    q8: Optional[str] = None
    q9: Optional[str] = None
    q10: Optional[str] = None
    q11: Optional[str] = None
    result: Optional[int] = None