from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from indexer import models as models
from indexer.types.tz_svls.tezos_big_maps.svls_key import SvlsKey
from indexer.types.tz_svls.tezos_big_maps.svls_value import SvlsValue


async def on_change(
    ctx: HandlerContext,
    svls: TezosBigMapDiff[SvlsKey, SvlsValue],
) -> None:
    if not svls.key: return
    svl_id = svls.key.root
    owner_address = svls.value.owner
    owner_vin = svls.value.VIN
    owner_brand = svls.value.brand
    owner_model = svls.value.model
    owner_year = svls.value.year    
    prev_owners_info = svls.value.prev_owners_info
    curr_owner_info = svls.value.curr_owner_info
    p_i = []
    for o in prev_owners_info:
        p_i.append({'address': o.address, 'cids': o.list})
    price = svls.value.price
    request = svls.value.request                                                                    
    acceptRequest = svls.value.acceptRequest
    ctx.logger.info(f"svl_id:{svl_id}")
    ctx.logger.info(f"Owner VIN:{owner_vin}")
    ctx.logger.info(f"Owner brand:{owner_brand}")
    ctx.logger.info(f"Owner model:{owner_model}")
    ctx.logger.info(f"Owner year:{owner_year}")
    ctx.logger.info(f"Owner address:{owner_address}")
    ctx.logger.info(f"Previous owners info:{p_i}")
    ctx.logger.info(f"Current owner info:{curr_owner_info}")
    ctx.logger.info(f"Price:{price}")
    ctx.logger.info(f"Request:{request}")
    ctx.logger.info(f"Accepted request:{acceptRequest}")
    ctx.logger.info(svl_id)
    holder = await models.Holder.get_or_none(id=svl_id)
    if holder is None:
        await models.Holder.create(
            id=svl_id, 
            address=owner_address,
            vin=owner_vin,
            brand=owner_brand,
            model=owner_model,
            year=owner_year,
            prev_owners_info=p_i,
            curr_owner_info=curr_owner_info,
            price=price,
            request=request,
            accept_request=acceptRequest
        )
    else:
        holder.address = owner_address
        holder.vin = owner_vin
        holder.brand = owner_brand
        holder.model = owner_model
        holder.year = owner_year
        holder.prev_owners_info = p_i
        holder.curr_owner_info = curr_owner_info
        holder.request = request
        holder.accept_request = acceptRequest
        await holder.save()