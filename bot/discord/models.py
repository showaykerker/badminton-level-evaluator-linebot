import dataclasses
from typing import Optional

from ..core.evaluator import Evaluator

@dataclasses.dataclass
class DiscordUser:
    discord_id: str
    name: str
    questionaire: Evaluator