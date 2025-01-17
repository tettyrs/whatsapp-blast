import os
# from dotenv import load_dotenv

# load_dotenv()

class Config():
    phoneNumId = os.getenv("PHONE_NUMBER_ID")
    messageLang = os.getenv("MSG_LANG")
    token = os.getenv("MSG_TOKEN")
    param1Name = os.getenv("PARAM1_NAME")