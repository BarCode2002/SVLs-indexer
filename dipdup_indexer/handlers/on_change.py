from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from dipdup_indexer import models as models
from dipdup_indexer.types.tz_svls.tezos_big_maps.svls_key import SvlsKey
from dipdup_indexer.types.tz_svls.tezos_big_maps.svls_value import SvlsValue
import gzip
import json
import re
from datetime import datetime
from io import BytesIO
import urllib.request

def check_json(json_data):
  if len(json_data)!=5: return False
  general_information_keys=['VIN', 'brand', 'model', 'year', 'transferDate', 'kilometers', 'mainPhotograph', 'state', 'photographs', 'weight', 'color', 'engine', 'power', 'shift', 'fuel', 'autonomy', 'climate', 'usage', 'storage', 'comments']
  maintenances_group_keys=['date', 'kilometers', 'name', 'responsible', 'pre', 'post', 'type', 'shrinked']
  maintenances_type_keys=['name', 'components', 'numComponents', 'pre', 'post', 'comments', 'shrinked']
  modifications_group_keys=['date', 'kilometers', 'name', 'responsible', 'pre', 'post', 'type', 'shrinked']
  modifications_type_keys=['name', 'components', 'numComponents', 'pre', 'post', 'comments', 'shrinked']
  defects_group_keys=['date', 'kilometers', 'cause', 'type', 'shrinked']
  defects_type_keys=['level', 'photographs', 'description', 'shrinked']
  repairs_group_keys=['date', 'kilometers', 'name', 'responsible', 'pre', 'post', 'defectsRepaired', 'numDefectsRepaired', 'type', 'shrinked']
  repairs_type_keys=['name', 'components', 'numComponents', 'pre', 'post', 'comments', 'shrinked']
  #url_lists='http://127.0.0.1:3000/mongo/lists?type='
  #url_models='http://127.0.0.1:3000/mongo/models?brand='
  #url_ipfs='http://127.0.0.1:8080/ipfs/'
  url_lists='http://host.docker.internal:3000/mongo/lists?type='#poner api-svc y ale
  url_models='http://host.docker.internal:3000/mongo/models?brand='
  url_ipfs='http://host.docker.internal:8080/ipfs/'
  
  try:
    if general_information_keys!=list(json_data[0].keys()): return False
    if not re.fullmatch(r'[A-Z0-9\-]+', json_data[0]['VIN']): return False
    with urllib.request.urlopen(url_lists+'brand') as brands:
      if not json_data[0]['brand'] in json.loads(brands.read()): return False
      with urllib.request.urlopen(url_models+json_data[0]['brand']) as models:
        if not json_data[0]['model'] in json.loads(models.read()): return False
    if not re.fullmatch(r'\d+', json_data[0]['year']): return False
    if not re.fullmatch(r'\d*', json_data[0]['kilometers'][0]): return False
    if json_data[0]['kilometers'][1]!='km' and json_data[0]['kilometers'][1]!='mi': return False
    if not datetime.strptime(json_data[0]['transferDate'], "%Y-%m-%dT%H:%M:%S.%fZ"): return False
    with urllib.request.urlopen(url_ipfs+json_data[0]['mainPhotograph']) as image:
      image.getcode()
    with urllib.request.urlopen(url_lists+'state') as states:
      data=json.loads(states.read())
      data.append('DataSVL.Forms.state')
      if not json_data[0]['state'] in data: return False
    if len(json_data[0]['photographs']) != 20: return False
    for cid in json_data[0]['photographs']:
      if cid!='':
        with urllib.request.urlopen(url_ipfs+cid) as image:
          image.getcode()
    if not re.fullmatch(r'\d*', json_data[0]['weight'][0]): return False
    if json_data[0]['weight'][1]!='kg' and json_data[0]['weight'][1]!='lb': return False
    if not re.fullmatch(r'[A-Za-z]*', json_data[0]['color']): return False
    #json_data[0]['engine'] can be whatever
    if not re.fullmatch(r'\d*', json_data[0]['power'][0]): return False
    if json_data[0]['power'][1]!='cv' and json_data[0]['power'][1]!='kW': return False
    with urllib.request.urlopen(url_lists+'shift') as shifts:
      data=json.loads(shifts.read())
      data.append('DataSVL.Forms.shift')
      if not json_data[0]['shift'] in data: return False
    with urllib.request.urlopen(url_lists+'fuel') as fuels:
      data=json.loads(fuels.read())
      data.append('DataSVL.Forms.fuel')
      if not json_data[0]['fuel'] in data: return False
    if not re.fullmatch(r'\d*', json_data[0]['autonomy'][0]): return False
    if json_data[0]['autonomy'][1]!='km' and json_data[0]['autonomy'][1]!='mi': return False
    with urllib.request.urlopen(url_lists+'climate') as climates:
      data=json.loads(climates.read())
      data.append('DataSVL.Forms.climate')
      if not json_data[0]['climate'] in data: return False
    with urllib.request.urlopen(url_lists+'usage') as usages:
      data=json.loads(usages.read())
      data.append('DataSVL.Forms.usage')
      if not json_data[0]['usage'] in data: return False
    with urllib.request.urlopen(url_lists+'storage') as storages:
      data=json.loads(storages.read())
      data.append('DataSVL.Forms.storage')
      if not json_data[0]['storage'] in data: return False
    #json_data[0]['comments']) can be whatever
  except Exception as e:
    print(f"Error checking general information in JSON: {e}")
    return False
    
  try:
    for i in range(len(json_data[1]['maintenances'])): #si maintenances no existe salta la excepcion, si maintenances = [](correcto tambien) pues no hace el loop
      if maintenances_group_keys!=list(json_data[1]['maintenances'][i].keys()): return False
      if not datetime.strptime(json_data[1]['maintenances'][i]['date'], "%Y-%m-%dT%H:%M:%S.%fZ"): return False
      if not re.fullmatch(r'\d*', json_data[1]['maintenances'][i]['kilometers'][0]): return False
      if json_data[1]['maintenances'][i]['kilometers'][1]!='km' and json_data[1]['maintenances'][i]['kilometers'][1]!='mi': return False
      #json_data[1]['maintenances'][i]['name'] can be whatever
      if len(json_data[1]['maintenances'][i]['responsible'])!=4: return False
      if ((json_data[1]['maintenances'][i]['responsible'][0]==None) or (json_data[1]['maintenances'][i]['responsible'][2]==None and (json_data[1]['maintenances'][i]['responsible'][0]==0 or json_data[1]['maintenances'][i]['responsible'][0]==2))): return False
      with urllib.request.urlopen(url_ipfs+json_data[1]['maintenances'][i]['responsible'][3]) as image:
        image.getcode()
      if len(json_data[1]['maintenances'][i]['pre'])!=20: return False
      for cid in json_data[1]['maintenances'][i]['pre']:
          if cid != '':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
      if len(json_data[1]['maintenances'][i]['post'])!=20: return False
      for cid in json_data[1]['maintenances'][i]['post']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
      if not isinstance(json_data[1]['maintenances'][i]['shrinked'], bool): return False
      if len(json_data[1]['maintenances'][i]['type']) == 0: return False #siempre habra un type como minimo
      for j in range(len(json_data[1]['maintenances'][i]['type'])):
        if maintenances_type_keys!=list(json_data[1]['maintenances'][i]['type'][j].keys()): return False
        #json_data[1]['maintenances'][i]['type'][j]['name'] can be whatever
        if len(json_data[1]['maintenances'][i]['type'][j]['components'])!=10: return False
        num_components=0
        for component in json_data[1]['maintenances'][i]['type'][j]['components']:
          if component!='': num_components+=1
        if num_components!=json_data[1]['maintenances'][i]['type'][j]['numComponents']: return False
        if len(json_data[1]['maintenances'][i]['type'][j]['pre'])!=20: return False
        for cid in json_data[1]['maintenances'][i]['type'][j]['pre']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        if len(json_data[1]['maintenances'][i]['type'][j]['post'])!=20: return False
        for cid in json_data[1]['maintenances'][i]['type'][j]['post']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        #json_data[1]['maintenances'][i]['type'][j]['comments'] can be whatever
        if not isinstance(json_data[1]['maintenances'][i]['type'][j]['shrinked'], bool): return False
  except Exception as e:
    print(f"Error checking maintenances in JSON: {e}")
    return False
  
  try:  
    for i in range(len(json_data[2]['modifications'])): #si modifications no existe salta la excepcion, si modifications = [](correcto tambien) pues no hace el loop
      if modifications_group_keys!=list(json_data[2]['modifications'][i].keys()): return False
      if not datetime.strptime(json_data[2]['modifications'][i]['date'], "%Y-%m-%dT%H:%M:%S.%fZ"): return False
      if not re.fullmatch(r'\d*', json_data[2]['modifications'][i]['kilometers'][0]): return False
      if json_data[2]['modifications'][i]['kilometers'][1]!='km' and json_data[2]['modifications'][i]['kilometers'][1]!='mi': return False
      #json_data[2]['modifications'][i]['name'] can be whatever
      if len(json_data[2]['modifications'][i]['responsible'])!=4: return False
      if ((json_data[2]['modifications'][i]['responsible'][0]==None) or (json_data[2]['modifications'][i]['responsible'][2]==None and (json_data[2]['modifications'][i]['responsible'][0]==0 or json_data[2]['modifications'][i]['responsible'][0]==2))): return False
      if json_data[2]['modifications'][i]['responsible'][2]==True and json_data[2]['modifications'][i]['responsible'][3]!='':
        with urllib.request.urlopen(url_ipfs+json_data[2]['modifications'][i]['responsible'][3]) as image:
          image.getcode()
      if len(json_data[2]['modifications'][i]['pre'])!=20: return False
      for cid in json_data[2]['modifications'][i]['pre']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
      if len(json_data[2]['modifications'][i]['post'])!=20: return False
      for cid in json_data[2]['modifications'][i]['post']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
      if not isinstance(json_data[2]['modifications'][i]['shrinked'], bool): return False
      if len(json_data[2]['modifications'][i]['type']) == 0: return False #siempre habra un type como minimo
      for j in range(len(json_data[2]['modifications'][i]['type'])):
        if modifications_type_keys!=list(json_data[2]['modifications'][i]['type'][j].keys()): return False
        #json_data[2]['modifications'][i]['type'][j]['name'] can be whatever
        if len(json_data[2]['modifications'][i]['type'][j]['components'])!=10: return False
        num_components=0
        for component in json_data[2]['modifications'][i]['type'][j]['components']:
          if component!='': num_components+=1
        if num_components!=json_data[2]['modifications'][i]['type'][j]['numComponents']: return False
        if len(json_data[2]['modifications'][i]['type'][j]['pre'])!=20: return False
        for cid in json_data[2]['modifications'][i]['type'][j]['pre']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        if len(json_data[2]['modifications'][i]['type'][j]['post'])!=20: return False
        for cid in json_data[2]['modifications'][i]['type'][j]['post']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        #json_data[2]['modifications'][i]['type'][j]['comments'] can be whatever
        if not isinstance(json_data[2]['modifications'][i]['type'][j]['shrinked'], bool): return False  
  except Exception as e:
    print(f"Error checking modifications in JSON: {e}")
    return False
  
  try:  
    for i in range(len(json_data[3]['defects'])): #si defects no existe salta la excepcion, si defects = [](correcto tambien) pues no hace el loop
      if defects_group_keys!=list(json_data[3]['defects'][i].keys()): return False
      if not datetime.strptime(json_data[3]['defects'][i]['date'], "%Y-%m-%dT%H:%M:%S.%fZ"): return False
      if not re.fullmatch(r'\d*', json_data[3]['defects'][i]['kilometers'][0]): return False
      if json_data[3]['defects'][i]['kilometers'][1]!='km' and json_data[3]['defects'][i]['kilometers'][1]!='mi': return False
      #json_data[3]['defects'][i]['cause'] can be whatever
      if not isinstance(json_data[3]['defects'][i]['shrinked'], bool): return False
      if len(json_data[3]['defects'][i]['type']) == 0: return False #siempre habra un type como minimo
      for j in range(len(json_data[3]['defects'][i]['type'])):
        if defects_type_keys!=list(json_data[3]['defects'][i]['type'][j].keys()): return False
        with urllib.request.urlopen(url_lists+'defectLevel') as levels:
          data=json.loads(levels.read())
          data.append('DataSVL.Forms.level')
          if not json_data[3]['defects'][i]['type'][j]['level'] in data: return False
        if len(json_data[3]['defects'][i]['type'][j]['photographs'])!=20: return False
        for cid in json_data[3]['defects'][i]['type'][j]['photographs']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        #json_data[3]['defects'][i]['type'][j]['description'] can be whatever
        if not isinstance(json_data[3]['defects'][i]['type'][j]['shrinked'], bool): return False
  except Exception as e:
    print(f"Error checking defects in JSON: {e}")
    return False
    
  try:  
    for i in range(len(json_data[4]['repairs'])): #si repairs no existe salta la excepcion, si repairs = [](correcto tambien) pues no hace el loop
      if repairs_group_keys!=list(json_data[4]['repairs'][i].keys()): return False
      if not datetime.strptime(json_data[4]['repairs'][i]['date'], "%Y-%m-%dT%H:%M:%S.%fZ"): return False
      if not re.fullmatch(r'\d*', json_data[4]['repairs'][i]['kilometers'][0]): return False
      if json_data[4]['repairs'][i]['kilometers'][1]!='km' and json_data[4]['repairs'][i]['kilometers'][1]!='mi': return False
      #json_data[4]['repairs'][i]['name'] can be whatever
      if len(json_data[4]['repairs'][i]['responsible'])!=4: return False
      if ((json_data[4]['repairs'][i]['responsible'][0]==None) or (json_data[4]['repairs'][i]['responsible'][2]==None and (json_data[4]['repairs'][i]['responsible'][0]==0 or json_data[4]['repairs'][i]['responsible'][0]==2))): return False
      if json_data[4]['repairs'][i]['responsible'][2]==True and json_data[4]['repairs'][i]['responsible'][3]!='':
        with urllib.request.urlopen(url_ipfs+json_data[4]['repairs'][i]['responsible'][3]) as image:
          image.getcode()
      if len(json_data[4]['repairs'][i]['pre'])!=20: return False
      for cid in json_data[4]['repairs'][i]['pre']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
      if len(json_data[4]['repairs'][i]['post'])!=20: return False
      for cid in json_data[4]['repairs'][i]['post']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
      if len(json_data[4]['repairs'][i]['type'][j]['defectsRepaired'])!=10: return False
      num_defectsRepaired=0
      for defectRepaired in json_data[4]['repairs'][i]['type'][j]['defectsRepaired']: 
        if defectRepaired[0]!=-1 and defectRepaired[1]!=-1 and defectRepaired[2]!=-1: num_defectsRepaired+=1
      if num_defectsRepaired!=json_data[4]['repairs'][i]['type'][j]['numDefectsRepaired']: return False #primero miro si coincide el numero de defects repaired completados
      for l in range(num_defectsRepaired): #luego miro que estan en las primeras posiciones(de 0 a num_defectsRepaired)
        if json_data[4]['repairs'][i]['type'][j]['defectsRepaired'][l][0]==-1 or json_data[4]['repairs'][i]['type'][j]['defectsRepaired'][l][1]==-1 or json_data[4]['repairs'][i]['type'][j]['defectsRepaired'][l][2]==-1: return False
      if not isinstance(json_data[4]['repairs'][i]['shrinked'], bool): return False
      if len(json_data[4]['repairs'][i]['type']) == 0: return False #siempre habra un type como minimo
      for j in range(len(json_data[4]['repairs'][i]['type'])):
        if repairs_type_keys!=list(json_data[4]['repairs'][i]['type'][j].keys()): return False
        #json_data[4]['repairs'][i]['type'][j]['name'] can be whatever
        if len(json_data[4]['repairs'][i]['type'][j]['components'])!=10: return False
        num_components=0
        for component in json_data[4]['repairs'][i]['type'][j]['components']:
          if component!='': num_components+=1
        if num_components!=json_data[4]['repairs'][i]['type'][j]['numComponents']: return False
        if len(json_data[4]['repairs'][i]['type'][j]['pre'])!=20: return False
        for cid in json_data[4]['repairs'][i]['type'][j]['pre']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        if len(json_data[4]['repairs'][i]['type'][j]['post'])!=20: return False
        for cid in json_data[4]['repairs'][i]['type'][j]['post']:
          if cid!='':
            with urllib.request.urlopen(url_ipfs+cid) as image:
              image.getcode()
        #json_data[4]['repairs'][i]['type'][j]['comments'] can be whatever
        if not isinstance(json_data[4]['repairs'][i]['type'][j]['shrinked'], bool): return False
  except Exception as e:
    print(f"Error checking repairs in JSON: {e}")
    return False
  
  return True

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

      svl_valid=True

      match = re.match(r"^(\d{2} \d{2} \d{4} \d{2}:\d{2}:\d{2}) (tz1[a-zA-Z0-9]{33})$", svl_key)
      if not match: 
        ctx.logger.info('Wrong svl_key pattern')
        svl_valid=False
      if svl_valid:
        date_part, address_part = match.groups()
        try:
          datetime.strptime(date_part, "%d %m %Y %H:%M:%S")
        except ValueError:
          ctx.logger.info('Date not valid in svl_key')
          svl_valid=False
      
      if not first_owner:
        for o in prev_owners_info:
          if svl_valid:
            for cid in o.list:
              if svl_valid:
                try: 
                  response = await local_ipfs.request(
                    method='get',
                    url=cid, 
                    timeout=1,
                  )
                  with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
                    json_data=json.load(gz_file)
                  if check_json(json_data):
                    num_maintenances+=len(json_data[1]['maintenances'])
                    num_modifications+=len(json_data[2]['modifications'])
                    for i in range(len(json_data[3]['defects'])):
                      for j in range(len(json_data[3]['defects'][i]['type'])):
                        if json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.cosmetic': num_cosmetic_defects+=1
                        elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.minor': num_minor_defects+=1
                        elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.moderate': num_moderate_defects+=1
                        elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.important': num_important_defects+=1
                        elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.critical': num_critical_defects+=1
                    num_repairs+=len(json_data[4]['repairs'])
                  else:
                    ctx.logger.info(f"JSON not valid {cid}")
                    svl_valid=False
                except Exception as e:
                  ctx.logger.info(f"CID not found: {cid} / {e}")
                  svl_valid=False
            p_o_i.append({'transferDate': o.timestamp, 'address': o.address, 'cids': o.list})
            if (o.list[0] != ''): num_owners+=len(o.list)

      if curr_owner_info==[]: svl_valid=False
      num_owners+=len(curr_owner_info)
      print(num_owners)
      for cid in curr_owner_info:
        if svl_valid and cid!='': #only possible when just transferred
          try: 
            response = await local_ipfs.request(
              method='get',
              url=cid,
              timeout=1,
            )
            with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
              json_data=json.load(gz_file)
            if check_json(json_data):
              num_maintenances+=len(json_data[1]['maintenances'])
              num_modifications+=len(json_data[2]['modifications'])
              for i in range(len(json_data[3]['defects'])):
                ctx.logger.info("F")
                for j in range(len(json_data[3]['defects'][i]['type'])):
                  if json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.cosmetic': num_cosmetic_defects+=1
                  elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.minor': num_minor_defects+=1
                  elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.moderate': num_moderate_defects+=1
                  elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.important': num_important_defects+=1
                  elif json_data[3]['defects'][i]['type'][j]['level']=='Lists.DefectLevel.critical': num_critical_defects+=1
              num_repairs+=len(json_data[4]['repairs'])
            else:
              ctx.logger.info(f"JSON not valid {cid}")
              svl_valid=False
          except Exception as e:
            ctx.logger.info(f"CID not found: {cid} / {e}")
            svl_valid=False

      if svl_valid:
        ctx.logger.info("SVL is valid")
        holder=await models.Holder.get_or_none(svl_key=svl_key)
        cid=''
        if (curr_owner_info[len(curr_owner_info)-1]!=''): cid=curr_owner_info[len(curr_owner_info)-1] #not just transferred
        elif (len(prev_owners_info[0].list)>0): cid=prev_owners_info[0].list[len(prev_owners_info[0].list)-1] #just transferred so get prev_owners value
        try: 
          response = await local_ipfs.request(
            method='get',
            url=cid, 
            timeout=1,
          )
          with gzip.GzipFile(fileobj=BytesIO(response)) as gz_file:
            json_data=json.load(gz_file)         
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
         
        except Exception as e: #este except no deberia pasar ya que se revisa antes, pero lo dejo por hay fallo de conexion
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
        if svl_valid and holder is None:
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
        elif svl_valid:
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