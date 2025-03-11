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
      svl_key=svls.key.root

      owner_address=svls.value.owner
      first_owner=svls.value.first_owner
      requester_address=svls.value.request                                                                    
      request_accepted=svls.value.acceptRequest
      curr_owner_info=svls.value.curr_owner_info
      prev_owners_info=svls.value.prev_owners_info
      svl_price = svls.value.price

      p_o_i = []
      num_owners=0
      num_maintenances=0
      num_modifications=0
      num_cosmetic_defects=0
      num_minor_defects=0
      num_moderate_defects=0
      num_important_defects=0
      num_critical_defects=0
      num_repairs=0
      local_ipfs = ctx.get_http_datasource('local_ipfs')

      for o in prev_owners_info:
        for cid in o.list:
          try: 
            response = await local_ipfs.request(
              method='get',
              url=cid, 
              timeout=1,
            )
            with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
              json_data = json.load(gz_file)
            num_maintenances+=len(json_data[1]['maintenances'])
            num_modifications+=len(json_data[2]['modifications'])
            for i in range(len(json_data[3]['defects'])):
              if json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.cosmetic': num_cosmetic_defects+=1
              elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.minor': num_minor_defects+=1
              elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.moderate': num_moderate_defects+=1
              elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.important': num_important_defects+=1
              elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.critical': num_critical_defects+=1
            num_repairs+=len(json_data[4]['repairs'])
          except Exception as e:
            ctx.logger.info(f"CID not found: {cid} / {e}")
        p_o_i.append({'transferDate': o.timestamp, 'address': o.address, 'cids': o.list})
        if (o.list[0] != ''): num_owners+=len(o.list)

      num_owners+=len(curr_owner_info)
      for cid in curr_owner_info:
        try: 
          response = await local_ipfs.request(
            method='get',
            url=cid, 
            timeout=1,
          )
          with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
            json_data = json.load(gz_file)
          num_maintenances+=len(json_data[1]['maintenances'])
          num_modifications+=len(json_data[2]['modifications'])
          for i in range(len(json_data[3]['defects'])):
            if json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.cosmetic': num_cosmetic_defects+=1
            elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.minor': num_minor_defects+=1
            elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.moderate': num_moderate_defects+=1
            elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.important': num_important_defects+=1
            elif json_data[3]['defects'][i]['type'][0]['level'] == 'Lists.DefectLevel.critical': num_critical_defects+=1
          num_repairs+=len(json_data[4]['repairs'])
        except Exception as e:
          ctx.logger.info(f"CID not found: {cid} / {e}")

      holder = await models.Holder.get_or_none(svl_key=svl_key)
      cid=''
      if (curr_owner_info[len(curr_owner_info)-1] != ''): cid=curr_owner_info[len(curr_owner_info)-1]
      else: cid = prev_owners_info[0].list[len(prev_owners_info[0].list)-1]
      try: 
        response = await local_ipfs.request(
            method='get',
            url=cid, 
            timeout=1,
        )
        with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
            json_data = json.load(gz_file)
        vin=json_data[0]['VIN']
        brand=json_data[0]['brand']
        model=json_data[0]['model']    
        year=int(json_data[0]['year'])
        kilometers=json_data[0]['kilometers']
        if (kilometers[0] != '' and kilometers[1] == 'mi'): kilometers=int(float(kilometers[0])*0.621371)
        elif (kilometers[0] != ''): kilometers=int(kilometers[0])
        else: kilometers=-1
        state=json_data[0]['state']
        weight=json_data[0]['weight']
        if (weight[0] != '' and weight[1] == 'lb'): weight=int(float(weight[0])*2.20462)
        elif (weight[0] != ''): weight=int(weight[0])
        else: weight=-1
        power=json_data[0]['power']
        if (power[0] != '' and power[1] == 'kW'): power=int(float(power[0])*1.34102)
        elif (power[0] != ''): power=int(power[0])
        else: power=-1
        shift=json_data[0]['shift']
        fuel=json_data[0]['fuel']
        autonomy=json_data[0]['autonomy']
        if (autonomy[0] != '' and autonomy[1] == 'mi'): autonomy=int(float(autonomy[0])*0.621371)
        elif (autonomy[0] != ''): autonomy=int(autonomy[0])
        else: autonomy=-1
        climate=json_data[0]['climate']
        usage=json_data[0]['usage']
        storage=json_data[0]['storage']
      except Exception as e:
        ctx.logger.info(f"CID not found: {e}")
        vin=''
        brand=''
        model=''
        year=-1
        kilometers=-1
        state=''
        weight=-1
        power=-1
        shift=''
        fuel=''
        autonomy=-1
        climate=''
        usage=''
        storage=''
      if holder is None:
        await models.Holder.create(
          svl_key=svl_key, 
          
          owner_address=owner_address,
          first_owner=first_owner,
          requester_address=requester_address,
          request_accepted=request_accepted,
          current_owner_info=curr_owner_info,
          previous_owners_info=p_o_i,
          svl_price=svl_price,

          vin=vin,
          brand=brand,
          model=model,
          year=year,
          kilometers=kilometers,
          state=state,
          weight=weight,
          power=power,
          shift=shift,
          fuel=fuel,
          autonomy=autonomy,
          climate=climate,
          usage=usage,
          storage=storage,
          num_owners=num_owners,
          num_maintenances=num_maintenances,
          num_modifications=num_modifications,
          num_cosmetic_defects=num_cosmetic_defects,
          num_minor_defects=num_minor_defects,
          num_moderate_defects=num_moderate_defects,
          num_important_defects=num_important_defects,
          num_critical_defects=num_critical_defects,
          num_repairs=num_repairs,
        )
      else:
        holder.owner_address=owner_address
        holder.first_owner=first_owner
        holder.requester_address=requester_address
        holder.request_accepted=request_accepted
        holder.current_owner_info=curr_owner_info
        holder.previous_owners_info=p_o_i
        holder.svl_price = svl_price

        holder.vin=vin
        holder.brand=brand
        holder.model=model
        holder.year=year
        holder.kilometers=kilometers
        holder.state=state
        holder.weight=weight
        holder.power=power
        holder.shift=shift
        holder.fuel=fuel
        holder.autonomy=autonomy
        holder.climate=climate
        holder.usage=usage
        holder.storage=storage
        holder.num_owners=num_owners
        holder.num_maintenances=num_maintenances
        holder.num_modifications=num_modifications
        holder.num_cosmetic_defects=num_cosmetic_defects
        holder.num_minor_defects=num_minor_defects
        holder.num_moderate_defects=num_moderate_defects
        holder.num_important_defects=num_important_defects
        holder.num_critical_defects=num_critical_defects
        holder.num_repairs=num_repairs
        await holder.save()