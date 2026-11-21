def assess_image(filename:str,caption:str='')->dict:
    """Safe fallback until a validated crop disease vision model is installed."""
    return {'available':False,'filename':filename,'caption':caption,'message':'No image diagnosis model is configured. Record crop, stage and symptoms; consult an extension officer before treatment.'}
