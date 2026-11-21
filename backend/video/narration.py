def subtitles(script:str)->list[dict]:
    return [{'index':i+1,'text':line.strip()} for i,line in enumerate(script.split('.') if script else []) if line.strip()]
