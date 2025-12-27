import sys
import os
import datetime
import storage
import vehicles
import customers
import reservations
import reports
DATA_DIR="data"
BACKUP_DIR="backups"
def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    v_list,c_list,r_list=storage.load_state(DATA_DIR)
    while True:
        print("\n--- Vehicle Rental System ---")
        print("1. Staff Login")
        print("2. Customer Login")
        print("3. Exit")
        choice=input("Select: ")
        if choice=="1":
            staff_menu(v_list,c_list,r_list)
        elif choice=="2":
            customer_menu(v_list,c_list,r_list)
        elif choice=="3":
            storage.save_state(DATA_DIR,v_list,c_list,r_list)
            print("Data saved. Exiting.")
            break
        else:
            print("Invalid choice.")
def staff_menu(v_list,c_list,r_list):
    while True:
        print("\n--- Staff Menu ---")
        print("1. Add Vehicle")
        print("2. List Vehicles")
        print("3. Add Customer")
        print("4. Create Reservation")
        print("5. Complete Rental")
        print("6. Reports")
        print("7. Backup Data")
        print("8. Back")
        choice=input("Select: ")
        if choice=="1":
            vid=input("ID: ")
            make=input("Make: ")
            model=input("Model: ")
            rate=float(input("Rate/Day: "))
            km_rate=float(input("Rate/KM: "))
            v_data={"id":vid,"make":make,"model":model,"status":"available","rate_per_day":rate,"rate_per_km":km_rate,"mileage":0}
            vehicles.add_vehicle(v_list,v_data)
            print("Vehicle added.")
        elif choice=="2":
            for v in v_list: print(v)
        elif choice=="3":
            cid=input("ID: ")
            name=input("Name: ")
            license_num=input("License: ")
            pin=input("PIN: ")
            c_data={"id":cid,"name":name,"license_number":license_num,"pin":pin}
            customers.register_customer(c_list,c_data)
            print("Customer added.")
        elif choice=="4":
            vid=input("Vehicle ID: ")
            cid=input("Customer ID: ")
            start=input("Start (YYYY-MM-DD): ")
            end=input("End (YYYY-MM-DD): ")
            if reservations.check_availability(r_list,vid,start,end):
                res_data={"vehicle_id":vid,"customer_id":cid,"start_date":start,"end_date":end}
                reservations.create_reservation(r_list,res_data,v_list)
                print("Reservation created.")
            else:
                print("Vehicle not available.")
        elif choice=="5":
            rid=input("Reservation ID: ")
            odo=float(input("End Odometer: "))
            for res in r_list:
                if res["id"]==rid:
                    v_id=res["vehicle_id"]
                    curr_v=next((v for v in v_list if v["id"]==v_id),None)
                    res["start_odometer"]=curr_v["mileage"]
                    res["end_odometer"]=odo
                    inv=reservations.calculate_invoice(res,{},curr_v)
                    res["invoice"]=inv
                    reservations.complete_rental(r_list,rid,{"end_odometer":odo},v_list)
                    curr_v["mileage"]=odo
                    print(f"Rental completed. Total: {inv['total']}")
        elif choice=="6":
            print(reports.revenue_summary(r_list,("2020-01-01","2030-01-01")))
        elif choice=="7":
            storage.backup_state(DATA_DIR,BACKUP_DIR)
            print("Backup created.")
        elif choice=="8":
            break
        storage.save_state(DATA_DIR,v_list,c_list,r_list)
def customer_menu(v_list,c_list,r_list):
    license_num=input("License: ")
    pin=input("PIN: ")
    user=customers.authenticate_customer(c_list,license_num,pin)
    if not user:
        print("Auth failed.")
        return
    while True:
        print(f"\nWelcome {user['name']}")
        print("1. My Reservations")
        print("2. Search Available Vehicles")
        print("3. Back")
        choice=input("Select: ")
        if choice=="1":
            for r in r_list:
                if r["customer_id"]==user["id"]: print(r)
        elif choice=="2":
            s=input("Start (YYYY-MM-DD): ")
            e=input("End (YYYY-MM-DD): ")
            avail=vehicles.list_available_vehicles(v_list,(s,e),r_list)
            for v in avail: print(v)
        elif choice=="3":
            break
if __name__=="__main__":
    main()