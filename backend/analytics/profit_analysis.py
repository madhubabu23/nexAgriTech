def estimate_revenue(quantity:float,price:float,costs:float=0)->dict:
    gross=quantity*price
    return {'gross_revenue':round(gross,2),'estimated_costs':round(costs,2),'estimated_profit':round(gross-costs,2),'fees_included':False}
