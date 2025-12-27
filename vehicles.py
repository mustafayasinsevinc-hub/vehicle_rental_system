import json
def load_vehicles(path):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_vehicles(path,vehicles):
    with open(path,'w') as f:
        json.dump(vehicles,f,indent=4)
def add_vehicle(vehicles,vehicle_data):
    vehicles.append(vehicle_data)
    return vehicle_data
def update_vehicle(vehicles,vehicle_id,updates):
    for vehicle in vehicles:
        if vehicle["id"]==vehicle_id:
            vehicle.update(updates)
            return vehicle
    return {}
def set_vehicle_status(vehicles,vehicle_id,status):
    for vehicle in vehicles:
        if vehicle["id"]==vehicle_id:
            vehicle["status"]=status
            return vehicle
    return {}
def list_available_vehicles(vehicles,rental_dates,reservations):
    available=[]
    start_req=rental_dates[0]
    end_req=rental_dates[1]
    for vehicle in vehicles:
        if vehicle["status"]!="available":
            continue
        is_booked=False
        for res in reservations:
            if res["vehicle_id"]==vehicle["id"] and res["status"]=="active":
                if not (end_req<=res["start_date"] or start_req>=res["end_date"]):
                    is_booked=True
                    break
        if not is_booked:
            available.append(vehicle)
    return available