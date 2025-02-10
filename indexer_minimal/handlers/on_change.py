from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from indexer_minimal import models as models
from indexer_minimal.types.tz_svls.tezos_big_maps.svls_key import SvlsKey
from indexer_minimal.types.tz_svls.tezos_big_maps.svls_value import SvlsValue


async def on_change(
    ctx: HandlerContext,
    svls: TezosBigMapDiff[SvlsKey, SvlsValue],
) -> None:
    if not svls.key: return
    svl_key = svls.key.root
    owner_address = svls.value.owner
    vin = svls.value.VIN
    brand = svls.value.brand
    model = svls.value.model
    year = svls.value.year    
    requester_address = svls.value.request                                                                    
    request_accepted = svls.value.acceptRequest
    curr_owner_info = svls.value.curr_owner_info
    prev_owners_info = svls.value.prev_owners_info
    p_o_i = []
    for o in prev_owners_info:
        p_o_i.append({'address': o.address, 'cids': o.list})
    svl_price = svls.value.price
   

    ctx.logger.info(svl_key)
    
    holder = await models.Holder.get_or_none(svl_key=svl_key)
    if holder is None:
        await models.Holder.create(
            svl_key=svl_key, 
            owner_address=owner_address,
            vin=vin,
            brand=brand,
            model=model,
            year=year,
            requester_address=requester_address,
            request_accepted=request_accepted,
            current_owner_info=curr_owner_info,
            previous_owners_info=p_o_i,
            svl_price=svl_price,
        )
    else:
        holder.owner_address = owner_address
        holder.vin = vin
        holder.brand = brand
        holder.model = model
        holder.year = year
        holder.requester_address = requester_address
        holder.request_accepted = request_accepted
        holder.current_owner_info = curr_owner_info
        holder.previous_owners_info = p_o_i
        holder.svl_price = svl_price
        await holder.save()