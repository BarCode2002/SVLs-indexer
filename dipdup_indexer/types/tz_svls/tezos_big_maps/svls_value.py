from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict


class PrevOwnersInfoItem(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    timestamp: str
    address: str
    list: List[str]


class SvlsValue(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    acceptRequest: bool
    curr_owner_info: List[str]
    first_owner: bool
    owner: str
    prev_owners_info: List[PrevOwnersInfoItem]
    price: str
    request: str