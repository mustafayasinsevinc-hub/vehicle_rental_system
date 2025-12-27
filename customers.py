import json
def load_customers(path):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_customers(path,customers):
    with open(path,'w') as f:
        json.dump(customers,f,indent=4)
def register_customer(customers,profile):
    customers.append(profile)
    return profile
def authenticate_customer(customers,license_number,pin):
    for customer in customers:
        if customer["license_number"]==license_number and customer["pin"]==pin:
            return customer
    return None
def update_customer_profile(customers,customer_id,updates):
    for customer in customers:
        if customer["id"]==customer_id:
            customer.update(updates)
            return customer
    return {}