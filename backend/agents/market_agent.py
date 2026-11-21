def compare_to_market(suggested_price:float,market_price:float|None)->dict:
    if market_price is None:return {'comparison':'unavailable','message':'No market observation for this crop.'}
    return {'comparison':'above' if suggested_price>market_price else 'below' if suggested_price<market_price else 'near','difference':round(suggested_price-market_price,2),'market_price':market_price}
