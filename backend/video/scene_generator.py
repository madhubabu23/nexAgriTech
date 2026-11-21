def scenes(script:str)->list[dict]:
    steps=[s.strip() for s in script.split(';') if s.strip()]
    return [{'scene':i+1,'caption':step,'visual_note':'Illustrative generated scene; do not present as real farm footage.'} for i,step in enumerate(steps)]
