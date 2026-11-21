def forecast(prices:list[float])->dict:
    if len(prices)<3:return {'available':False,'message':'At least three observed periods are needed.'}
    delta=prices[-1]-prices[-2]
    return {'available':True,'next_period_estimate':round(prices[-1]+delta,2),'method':'naive last-change baseline','not_financial_advice':True}
