def validate_order_lines(lines:list[dict],inventory:dict[int,float])->None:
    for line in lines:
        available=inventory.get(int(line['product_id']),0)
        if float(line['quantity'])<=0 or float(line['quantity'])>available:raise ValueError('Requested quantity is unavailable')
