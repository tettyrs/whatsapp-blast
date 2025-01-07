import requests
import json, os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
from req import WhatsappBlastRequest
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

@app.post("/blast")
def blast_whatsapp(req: WhatsappBlastRequest):
    reqDict = req.dict()
    reqDict["phone_number"] = "628xxx"
    logger.info("Request payload : {}".format(reqDict))

    phoneNum = req.phone_number.strip()
    templateName = req.template_name.strip()
    statusCode = 0

    url = os.getenv("META_ENDPOINT")
    messageLang = os.getenv("MSG_LANG")
    token = os.getenv("MSG_TOKEN")

    reqTmpl = {
    "messaging_product": "whatsapp",
    "to": "",
    "type": "template",
    "template": {
        "name": "",
        "language": {
        "code": ""
        }
    }
    }

    reqTmpl["to"] = phoneNum
    reqTmpl["template"]["name"] = templateName
    reqTmpl["template"]["language"]["code"] =  messageLang


    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(token)
    }
   
    response = requests.post(url, headers=headers, data=json.dumps(reqTmpl))
    reqTmpl["to"] = "628xxx"
    logger.info("Sending message to customer. Send this request payload to Meta : {}".format(reqTmpl))
    strRes = response.text
    jsonRes = json.loads(strRes)
    
    if jsonRes.get("error"):
        content = {"errorCode": f"{response.status_code}", "errorMessage":jsonRes.get("error").get("message"), "status": "Failed"}
        statusCode = response.status_code
    elif jsonRes.get("messages")[0].get("id") != None or jsonRes.get("messages")[0].get("id") != "":
        content = {"errorCode":"200", "errorMessage":"", "status": "Success"}
        statusCode = 200
        jsonRes["contacts"][0]["input"] = "628xxx"
        jsonRes["contacts"][0]["wa_id"] = "628xxx"
        jsonRes["messages"][0]["id"] = "xxx"
    
   
    logger.info("Response from Meta : {}".format(jsonRes))
    logger.info("Process Finised. Response payload : {}".format(content))
    
    return JSONResponse(content=content, status_code=statusCode)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)