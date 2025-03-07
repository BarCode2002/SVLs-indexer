from dipdup import fields
from dipdup.models import Model

class Holder(Model):
    svl_key = fields.CharField(max_length=200, primary_key=True)

    owner_address=fields.TextField()
    requester_address=fields.TextField()
    request_accepted=fields.BooleanField()
    current_owner_info=fields.JSONField()
    previous_owners_info=fields.JSONField()
    svl_price=fields.CharField(max_length=200)

    vin=fields.TextField()
    brand=fields.TextField()
    model=fields.TextField()
    year=fields.TextField()
    kilometers=fields.TextField()
    state=fields.TextField()
    power=fields.TextField()
    shift=fields.TextField()
    fuel=fields.TextField()
    autonomy=fields.TextField()
    climate=fields.TextField()
    usage=fields.TextField()
    storage=fields.TextField()
    num_owners=fields.TextField()
    num_maintenances=fields.TextField()
    num_modifications=fields.TextField()
    num_defects=fields.TextField()
    num_repairs=fields.TextField()

