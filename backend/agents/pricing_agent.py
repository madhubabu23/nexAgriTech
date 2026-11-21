def suggest_price(costs:dict, quantity:float, desired_profit:float)->dict:
    total=sum(float(v or 0) for v in costs.values())
    return {'total_cost':round(total,2),'cost_per_unit':round(total/quantity,2),'suggested_price':round((total+desired_profit)/quantity,2),'desired_profit':round(desired_profit,2)}
