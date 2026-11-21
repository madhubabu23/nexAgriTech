def current_weather(location:str)->dict:
    """Weather provider adapter placeholder; no live source is configured."""
    return {'available':False,'location':location,'message':'Configure a weather provider API key to show live forecasts.'}
