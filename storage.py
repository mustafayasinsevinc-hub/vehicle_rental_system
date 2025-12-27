import json
import os
import shutil
import datetime
def load_state(base_dir):
    vehicles_path=os.path.join(base_dir,"vehicles.json")
    customers_path=os.path.join(base_dir,"customers.json")
    reservations_path=os.path.join(base_dir,"reservations.json")
    vehicles=[]
    customers=[]
    reservations=[]
    if os.path.exists(vehicles_path):
        with open(vehicles_path,'r') as f:
            vehicles=json.load(f)
    if os.path.exists(customers_path):
        with open(customers_path,'r') as f:
            customers=json.load(f)
    if os.path.exists(reservations_path):
        with open(reservations_path,'r') as f:
            reservations=json.load(f)
    return vehicles,customers,reservations
def save_state(base_dir,vehicles,customers,reservations):
    vehicles_path=os.path.join(base_dir,"vehicles.json")
    customers_path=os.path.join(base_dir,"customers.json")
    reservations_path=os.path.join(base_dir,"reservations.json")
    with open(vehicles_path,'w') as f:
        json.dump(vehicles,f,indent=4)
    with open(customers_path,'w') as f:
        json.dump(customers,f,indent=4)
    with open(reservations_path,'w') as f:
        json.dump(reservations,f,indent=4)
def backup_state(base_dir,backup_dir):
    timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    current_backup_dir=os.path.join(backup_dir,f"backup_{timestamp}")
    os.makedirs(current_backup_dir,exist_ok=True)
    shutil.copy(os.path.join(base_dir,"vehicles.json"),current_backup_dir)
    shutil.copy(os.path.join(base_dir,"customers.json"),current_backup_dir)
    shutil.copy(os.path.join(base_dir,"reservations.json"),current_backup_dir)
    return [current_backup_dir]
def validate_reservation(reservation):
    required_fields=["id","vehicle_id","customer_id","start_date","end_date"]
    for field in required_fields:
        if field not in reservation:
            return False
    return True