"""Optional vision-capable advisor. Only calls an external model when configured."""
import json, os, urllib.request, urllib.error
from backend.agents.farming_agent import answer as fallback_answer

def advise(question:str,language:str,media:list[dict])->dict:
    key=os.getenv('OPENAI_API_KEY','').strip();model=os.getenv('OPENAI_MODEL','').strip()
    if not key or not model:
        return {'answer':fallback_answer(question,language),'provider':'offline guidance','media_analyzed':False,'note':'No AI/vision provider is configured. Attachments are saved for review, but this demo cannot inspect them.'}
    lang={'en':'English','te':'Telugu','hi':'Hindi'}.get(language,'English')
    content=[{'type':'text','text':f"Farmer's crop question: {question}\nRespond in {lang}. Be concise, practical and organic-first. Treat photos as uncertain visual evidence, state what is uncertain, ask for missing context, and never prescribe risky chemical doses. Recommend local expert confirmation for serious disease or pesticide decisions."}]
    for item in media:
        image=item.get('preview_data_url') if item.get('mime_type','').startswith('video/') else item.get('data_url')
        if image and image.startswith('data:image/'):
            content.append({'type':'text','text':f"Attached crop image/frame: {item.get('name','uploaded media')}"})
            content.append({'type':'image_url','image_url':{'url':image,'detail':'low'}})
    payload=json.dumps({'model':model,'messages':[{'role':'user','content':content}],'max_tokens':650}).encode()
    req=urllib.request.Request(os.getenv('OPENAI_API_BASE','https://api.openai.com/v1/chat/completions'),data=payload,headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=35) as response:result=json.loads(response.read())
        text=result['choices'][0]['message']['content']
        return {'answer':text,'provider':model,'media_analyzed':any(i.get('mime_type','').startswith('image/') or (i.get('mime_type','').startswith('video/') and i.get('preview_data_url')) for i in media),'note':'AI guidance may be wrong. Confirm diagnoses and treatments with a local agriculture professional.'}
    except (urllib.error.URLError,TimeoutError,KeyError,ValueError) as exc:
        return {'answer':fallback_answer(question,language),'provider':'offline fallback','media_analyzed':False,'note':f'Configured AI provider unavailable ({type(exc).__name__}). Attachments were stored; fallback guidance shown.'}
