from pydantic import BaseModel
from typing import Optional


class WhatsappBlastRequest(BaseModel):
    phone_number:str
    template_name:str
    param1:Optional[str]=None
    param2:Optional[str]=None
    param3:Optional[str]=None