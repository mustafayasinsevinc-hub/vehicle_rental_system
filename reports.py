from datetime import datetime
def utilization_report(reservations,vehicles,period):
    total_days=0
    rented_days=0
    start_p=datetime.strptime(period[0],"%Y-%m-%d")
    end_p=datetime.strptime(period[1],"%Y-%m-%d")
    period_len=(end_p-start_p).days
    if period_len==0: period_len=1
    for res in reservations:
        if res["status"] in ["active","completed"]:
            r_start=datetime.strptime(res["start_date"],"%Y-%m-%d")
            r_end=datetime.strptime(res["end_date"],"%Y-%m-%d")
            overlap_start=max(start_p,r_start)
            overlap_end=min(end_p,r_end)
            if overlap_start<overlap_end:
                rented_days+=(overlap_end-overlap_start).days
    total_capacity=len(vehicles)*period_len
    if total_capacity==0: return {"utilization_pct":0}
    return {"utilization_pct":(rented_days/total_capacity)*100}
def revenue_summary(reservations,period):
    total_revenue=0
    for res in reservations:
        if res.get("invoice") and res["status"]=="completed":
            total_revenue+=res["invoice"].get("total",0)
    return {"total_revenue":total_revenue}
def upcoming_returns(reservations,reference_date):
    returns=[]
    for res in reservations:
        if res["status"]=="active" and res["end_date"]>=reference_date:
            returns.append(res)
    return returns
def export_report(report,filename):
    with open(filename,'w') as f:
        f.write(str(report))
    return filename