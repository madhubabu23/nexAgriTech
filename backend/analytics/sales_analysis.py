def summarize(orders:list[dict],products:list[dict])->dict:
    return {'orders':len(orders),'gross_revenue':round(sum(float(x['total']) for x in orders),2),'active_listings':len(products),'stock_units':round(sum(float(x['quantity']) for x in products),2)}
