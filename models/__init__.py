from dipdup import fields
from dipdup.models import Model

class Holder(Model):
    svl_key = fields.CharField(max_length=100, primary_key=True)
    
    vin = fields.TextField()
    brand = fields.TextField()
    model = fields.TextField()
    year = fields.TextField()

    vehicle_type = fields.TextField()
    kilometers = fields.TextField()
    shift = fields.TextField()
    fuel = fields.TextField()
    power = fields.TextField()
    color = fields.TextField()
    state = fields.TextField()
    autonomy = fields.TextField()
    climate = fields.TextField()
    usage = fields.TextField()
    storage = fields.TextField()

    requester_address = fields.TextField()
    request_accepted = fields.BooleanField()
    previous_owners_info = fields.JSONField()
    current_owner_info = fields.JSONField()
    svl_price = fields.CharField(max_length=100)