from backend.agents.pricing_agent import suggest_price

def price_for_listing(costs, saleable_quantity, profit):
    return suggest_price(costs, saleable_quantity, profit)
