"""Request schemas used by the API."""
from pydantic import BaseModel, Field
from typing import Optional

class FarmerIn(BaseModel): name:str; farm_name:str=''; phone:str=''; location:str=''; acres:float=0; language:str='en'
class CropIn(BaseModel): name:str; variety:str=''; acres:float=Field(ge=0); stage:str='Sowing'; planted_on:str=''; notes:str=''
class ProductIn(BaseModel): name:str; category:str='Vegetables'; price:float=Field(gt=0); quantity:float=Field(ge=0); unit:str='kg'; description:str=''; harvest_date:str=''; practices:str=''; certification:str='farmer_declared'; nutrition:str='Nutrition data unavailable'; emoji:str='🥬'
class TaskIn(BaseModel): title:str; crop:str=''; due_date:str=''
class OrderLine(BaseModel): product_id:int; quantity:float=Field(gt=0)
class OrderIn(BaseModel): customer:str=''; phone:str=''; address:str=''; items:list[OrderLine]
class PriceIn(BaseModel): crop:str=''; quantity:float=Field(gt=0); profit:float=0; seed:float=0; fertilizer:float=0; labor:float=0; water:float=0; packaging:float=0; transport:float=0
class LessonIn(BaseModel): crop:str; kind:str='recipe'; language:str='en'; title:str=''
class ReviewIn(BaseModel): customer:str; rating:int=Field(ge=1,le=5); body:str
class CustomerSignup(BaseModel): name:str=Field(min_length=2,max_length=100); email:str; password:str=Field(min_length=8,max_length=200); phone:str=''; address:str=''
class CustomerLogin(BaseModel): email:str; password:str
class CustomerRegisterIn(BaseModel): name:str=Field(min_length=2,max_length=100); email:str; password:str=Field(min_length=8,max_length=200); phone:str=''; address:str=''
class CustomerLoginIn(BaseModel): email:str; password:str
class MediaItem(BaseModel): name:str; mime_type:str; data_url:str; preview_data_url:Optional[str]=None
class AdviceIn(BaseModel): question:str; language:str='en'; media:list[MediaItem]=Field(default_factory=list); media_consent:bool=False
