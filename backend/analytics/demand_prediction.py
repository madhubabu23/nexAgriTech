def demand_signal(sold_units:float,available_units:float)->dict:
    if available_units<=0:return {'signal':'out_of_stock','basis':'current inventory only'}
    ratio=sold_units/available_units
    return {'signal':'high' if ratio>2 else 'steady' if ratio>.5 else 'low','basis':'simple demo ratio; not a forecast'}
