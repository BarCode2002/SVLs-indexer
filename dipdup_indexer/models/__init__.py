from dipdup import fields
from dipdup.models import Model

class Holder(Model):
    svl_key = fields.CharField(max_length=100, primary_key=True)
    owner_address = fields.TextField()
    vin = fields.TextField()
    brand = fields.TextField()
    model = fields.TextField()
    year = fields.TextField()
    requester_address = fields.TextField()
    request_accepted = fields.BooleanField()
    current_owner_info = fields.JSONField()
    previous_owners_info = fields.JSONField()
    svl_price = fields.CharField(max_length=100)