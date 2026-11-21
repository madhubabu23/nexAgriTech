LANGUAGES={'en':'English','te':'Telugu','hi':'Hindi'}
def language_name(code:str)->str:return LANGUAGES.get(code,'English')
def translate(text:str,target_language:str)->dict:
    return {'text':text,'language':target_language,'translated':False,'message':'Configure a reviewed Telugu/Hindi translation provider; untranslated content is returned as-is.'}
