import json
import os


def load_vehicles(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_vehicles(path: str, vehicles: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(vehicles, f, indent=4)


def add_vehicle(vehicles: list, vehicle_data: dict) -> dict:
    for v in vehicles:
        if v["id"] == vehicle_data["id"]:
            raise ValueError("This ID has been using already.")

    vehicles.append(vehicle_data)
    return vehicle_data


def update_vehicle(vehicles: list, vehicle_id: str, updates: dict) -> dict:
    for v in vehicles:
        if v["id"] == vehicle_id:
            v.update(updates)
            return v
    raise ValueError("Vehicle doesn't found.")


def set_vehicle_status(vehicles: list, vehicle_id: str, status: str) -> dict:
    allowed = ["available", "maintenance", "rented"]
    if status not in allowed:
        raise ValueError("Invalid status.")

    for v in vehicles:
        if v["id"] == vehicle_id:
            v["status"] = status
            return v

    raise ValueError("Vehicle doesn't found.")


def list_available_vehicles(
    vehicles: list,
    rental_dates: tuple[str, str],
    vehicle_type: str | None = None
) -> list:
    result = []

    for v in vehicles:
        if v["status"] != "available":
            continue
        if vehicle_type and v["type"] != vehicle_type:
            continue
        result.append(v)

    return result