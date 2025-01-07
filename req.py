from pydantic import BaseModel
from typing import Optional


class WhatsappBlastRequest(BaseModel):
    phone_number:str
    template_name:str