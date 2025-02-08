from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from indexer import models as models
from indexer.types.tz_svls.tezos_big_maps.svls_key import SvlsKey
from indexer.types.tz_svls.tezos_big_maps.svls_value import SvlsValue


async def on_change(
    ctx: HandlerContext,
    svls: BigMapDiff[SvlsKey, SvlsValue],
) -> None:
    ...