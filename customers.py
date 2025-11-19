import json
import os


def load_customers(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_customers(path: str, customers: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=4)


def register_customer(customers: list, profile: dict) -> dict:
    # Basit doğrulamalar
    if len(profile["pin"]) != 4:
        raise ValueError("PIN must have 4 digit.")

    for c in customers:
        if c["license_number"] == profile["license_number"]:
            raise ValueError("This licence number has already in use.")

    customers.append(profile)
    return profile


def authenticate_customer(customers: list, license_number: str, pin: str):
    for c in customers:
        if c["license_number"] == license_number and c["pin"] == pin:
            return c
    return None


def update_customer_profile(customers: list, customer_id: str, updates: dict) -> dict:
    for c in customers:
        if c["id"] == customer_id:
            c.update(updates)
            return c

    raise ValueError("Customer doesn't found.")
