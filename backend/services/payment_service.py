def create_payment(total:float)->dict:
    return {'mode':'demo','payable':total,'message':'No payment provider configured. Do not collect real payments through this adapter.'}
