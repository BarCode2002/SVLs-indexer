from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from dipdup_indexer import models as models
from dipdup_indexer.types.tz_svls.tezos_big_maps.svls_key import SvlsKey
from dipdup_indexer.types.tz_svls.tezos_big_maps.svls_value import SvlsValue
import gzip
import json
from io import BytesIO

async def on_change(
    ctx: HandlerContext,
    svls: TezosBigMapDiff[SvlsKey, SvlsValue],
) -> None:
        if not svls.key: return
        svl_key=svls.key.root
        owner_address=svls.value.owner
        vin=svls.value.VIN  
        requester_address=svls.value.request                                                                    
        request_accepted=svls.value.acceptRequest
        curr_owner_info=svls.value.curr_owner_info
        prev_owners_info=svls.value.prev_owners_info
        p_o_i = []
        for o in prev_owners_info:
            p_o_i.append({'transferDate': o.timestamp, 'address': o.address, 'cids': o.list})
        svl_price = svls.value.price

        holder = await models.Holder.get_or_none(svl_key=svl_key)

        if (curr_owner_info[len(curr_owner_info)-1] != ''):
            local_ipfs = ctx.get_http_datasource('local_ipfs')
            response = await local_ipfs.request(
                method='get',
                url=curr_owner_info[len(curr_owner_info)-1], 
            )
            with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
                json_data = json.load(gz_file)
            ctx.logger.info(json_data)
            brand=json_data[0]['brand']
            model=json_data[0]['model']    
            year=json_data[0]['year']
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
                holder.owner_address=owner_address
                holder.vin=vin
                holder.brand=brand
                holder.model=model
                holder.year=year
                holder.requester_address=requester_address
                holder.request_accepted=request_accepted
                holder.current_owner_info=curr_owner_info
                holder.previous_owners_info=p_o_i
                holder.svl_price = svl_price
                await holder.save()
        else:
            holder.owner_address=owner_address
            holder.vin=vin
            holder.requester_address=requester_address
            holder.request_accepted=request_accepted
            holder.current_owner_info=curr_owner_info
            holder.previous_owners_info=p_o_i
            holder.svl_price = svl_price
            await holder.save()