from pydantic import BaseModel
from pydantic.types import conint


class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)  # allow selection only for 0 and 1
