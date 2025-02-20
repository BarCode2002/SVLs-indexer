from __future__ import annotations

from pydantic import RootModel


class SvlsKey(RootModel[str]):
    root: str