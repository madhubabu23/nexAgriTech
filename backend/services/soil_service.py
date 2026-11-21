def soil_guidance(ph:float|None=None,organic_carbon:float|None=None)->dict:
    if ph is None:return {'available':False,'message':'Enter measured soil values or connect a Soil Health Card data source.'}
    return {'available':True,'ph':ph,'organic_carbon':organic_carbon,'message':'Interpret measurements with a local soil laboratory or extension officer.'}
