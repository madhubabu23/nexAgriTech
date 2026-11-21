def available_stock(quantity:float,active:bool=True)->dict:
    return {'quantity':max(0,float(quantity)),'available':bool(active and quantity>0)}
