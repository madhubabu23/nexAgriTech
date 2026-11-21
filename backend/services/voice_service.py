def narration_script(text:str,language:str)->dict:
    return {'text':text,'language':language,'provider':'browser speech synthesis','audio_generated':False}
