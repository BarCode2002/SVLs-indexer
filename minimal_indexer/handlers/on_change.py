from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from minimal_indexer import models as models
from minimal_indexer.types.tz_svls.tezos_big_maps.svls_key import SvlsKey
from minimal_indexer.types.tz_svls.tezos_big_maps.svls_value import SvlsValue


async def on_change(
    ctx: HandlerContext,
    svls: TezosBigMapDiff[SvlsKey, SvlsValue],
) -> None:
        if not svls.key: return
        svl_key = svls.key.root
        owner_address = svls.value.owner
        vin = svls.value.VIN  
        requester_address = svls.value.request                                                                    
        request_accepted = svls.value.acceptRequest
        curr_owner_info = svls.value.curr_owner_info
        prev_owners_info = svls.value.prev_owners_info
        p_o_i = []
        for o in prev_owners_info:
            #ctx.logger.info(o)
            p_o_i.append({'transferData': o.timestamp, 'address': o.address, 'cids': o.list})
        svl_price = svls.value.price

        holder = await models.Holder.get_or_none(svl_key=svl_key)
        ctx.logger.info(curr_owner_info[0])
        if (curr_owner_info[0] != ''):
            local_ipfs = ctx.get_http_datasource('local_ipfs')
            response = await local_ipfs.request(
                method='get',
                url=curr_owner_info[0], 
            )
            ctx.logger.info(response[0]['brand'])
            ctx.logger.info(response[0]['year'])
            ctx.logger.info(response[0]['kilometers'])
            if holder is None:
                await models.Holder.create(
                    svl_key=svl_key, 
                    owner_address=owner_address,
                    vin=vin,
                    brand=response[0]['brand'],
                    model=response[0]['model'],
                    year=response[0]['year'],
                    requester_address=requester_address,
                    request_accepted=request_accepted,
                    current_owner_info=curr_owner_info,
                    previous_owners_info=p_o_i,
                    svl_price=svl_price,
                )
            else:
                holder.owner_address = owner_address
                holder.vin = vin,
                holder.brand=response[0]['brand'],
                holder.model=response[0]['model'],
                holder.year=response[0]['year'],      
                holder.requester_address = requester_address
                holder.request_accepted = request_accepted
                holder.current_owner_info = curr_owner_info
                holder.previous_owners_info = p_o_i
                holder.svl_price = svl_price
                await holder.save()
        else:
            if holder is None:
                await models.Holder.create(
                    svl_key=svl_key, 
                    owner_address=owner_address,
                    vin=vin,
                    brand='',
                    model='',
                    year='',
                    requester_address=requester_address,
                    request_accepted=request_accepted,
                    current_owner_info=curr_owner_info,
                    previous_owners_info=p_o_i,
                    svl_price=svl_price,
                )
            else:
                holder.owner_address = owner_address
                holder.vin = vin
                holder.requester_address = requester_address
                holder.request_accepted = request_accepted
                holder.current_owner_info = curr_owner_info
                holder.previous_owners_info = p_o_i
                holder.svl_price = svl_price
                await holder.save()



#ctx.logger.info(len(response[1]['maintenances']))
#if (len(response[1]['maintenances']) > 0):
#for i in range(len(response[1]['maintenances'])):
#ctx.logger.info(len(response[1]['maintenances'][i]['type']))