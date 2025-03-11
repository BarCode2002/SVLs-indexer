from dipdup import fields
from dipdup.models import Model

class Holder(Model):
  svl_key = fields.CharField(max_length=200, primary_key=True)

  owner_address=fields.TextField()
  first_owner=fields.BooleanField()
  requester_address=fields.TextField()
  request_accepted=fields.BooleanField()
  current_owner_info=fields.JSONField()
  previous_owners_info=fields.JSONField()
  svl_price=fields.CharField(max_length=200)

  vin=fields.TextField()
  brand=fields.TextField()
  model=fields.TextField()
  year=fields.IntField()
  kilometers=fields.IntField()
  state=fields.TextField()
  weight=fields.IntField()
  power=fields.IntField()
  shift=fields.TextField()
  fuel=fields.TextField()
  autonomy=fields.IntField()
  climate=fields.TextField()
  usage=fields.TextField()
  storage=fields.TextField()
  num_owners=fields.IntField()
  num_maintenances=fields.IntField()
  num_modifications=fields.IntField()
  num_cosmetic_defects=fields.IntField()
  num_minor_defects=fields.IntField()
  num_moderate_defects=fields.IntField()
  num_important_defects=fields.IntField()
  num_critical_defects=fields.IntField()
  num_repairs=fields.IntField()

