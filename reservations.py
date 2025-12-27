import uuid
from datetime import datetime
def create_reservation(reservations,reservation_data,vehicles):
    reservation_data["id"]=str(uuid.uuid4())
    reservation_data["status"]="active"
    reservations.append(reservation_data)
    return reservation_data
def check_availability(reservations,vehicle_id,start_date,end_date):
    for res in reservations:
        if res["vehicle_id"]==vehicle_id and res["status"]=="active":
            if not (end_date<=res["start_date"] or start_date>=res["end_date"]):
                return False
    return True
def cancel_reservation(reservations,reservation_id):
    for res in reservations:
        if res["id"]==reservation_id:
            res["status"]="cancelled"
            return True
    return False
def complete_rental(reservations,reservation_id,return_data,vehicles):
    for res in reservations:
        if res["id"]==reservation_id:
            res["status"]="completed"
            res.update(return_data)
            return res
    return {}
def calculate_invoice(reservation,pricing_rules,vehicle):
    fmt="%Y-%m-%d"
    d1=datetime.strptime(reservation["start_date"],fmt)
    d2=datetime.strptime(reservation["end_date"],fmt)
    days=(d2-d1).days
    if days<1: days=1
    base_cost=days*vehicle.get("rate_per_day",0)
    km_cost=0
    if "end_odometer" in reservation and "start_odometer" in reservation:
        dist=reservation["end_odometer"]-reservation["start_odometer"]
        km_cost=dist*vehicle.get("rate_per_km",0)
    total=base_cost+km_cost
    invoice={
        "reservation_id":reservation["id"],
        "days":days,
        "base_cost":base_cost,
        "km_cost":km_cost,
        "total":total
    }
    return invoice