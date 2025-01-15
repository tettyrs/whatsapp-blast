import requests
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
from req import WhatsappBlastRequest
from configs import Config

app = FastAPI()
CONFIG = Config()

@app.post("/blast")
def blast_whatsapp(req: WhatsappBlastRequest):
    try:
        phoneNumId = CONFIG.phoneNumId
        messageLang = CONFIG.messageLang
        token = CONFIG.token
        param1Name = CONFIG.param1Name

        reqDict = req.dict()
        reqDict["phone_number"] = "628xxx"
        logger.info("Request payload : {}".format(reqDict))

        phoneNum = req.phone_number.strip()
        templateName = req.template_name.strip()
        param1 = req.param1.strip() if req.param1 != None else req.param1
        param2 = req.param2.strip() if req.param2 != None else req.param2
        param3 = req.param3.strip() if req.param3 != None else req.param3
        statusCode = 0
        
        url =  "https://graph.facebook.com/v21.0/{}/messages".format(phoneNumId)
        
        if templateName == "hello_world":
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
            

            
        else:
            reqTmpl = {
            "messaging_product": "whatsapp",
            "to": "",
            "type": "template",
            "template": {
                "name": "",
                "language": {
                "code": ""  
                },
                "components": [
                {
                    "type": "body",
                    "parameters": [{
                        "type": "text",
                        "parameter_name": "",
                        "text": param1
                    }]
                }
                ]
            }
            }
            
        reqTmpl["to"] = phoneNum
        reqTmpl["template"]["name"] = templateName
        reqTmpl["template"]["language"]["code"] =  messageLang
        reqTmpl["template"]["components"][0]["parameters"][0]["parameter_name"]= param1Name
        if param2:
            reqTmpl["template"]["components"][1]["parameters"].append({
            "type": "text",
            "parameter_name":"param2",
            "text": param2
        })
        if param3:
            reqTmpl["template"]["components"][2]["parameters"].append({
            "type": "text",
            "parameter_name":"param3",
            "text": param3
        })
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
        }
    
        response = requests.post(url, headers=headers, data=json.dumps(reqTmpl, indent=4))
        reqTmpl["to"] = "628xxx"
        logger.info("Sending message to customer. Send this request payload to Meta : {}".format(reqTmpl))
        strRes = response.text
        jsonRes = json.loads(strRes)


        
        if 'wa_id' not in strRes:
            content = {"errorCode": f"{response.status_code}", "errorMessage":jsonRes.get("error").get("message"), "status": "Failed"}
            statusCode = response.status_code
            logger.error("{}".format(jsonRes.get("error").get("message")))
        else:
            content = {"errorCode":"200", "errorMessage":"", "status": "Success"}
            statusCode = 200
            logger.info("Message sent to customer")
            jsonRes["contacts"][0]["input"] = "628xxx"
            jsonRes["contacts"][0]["wa_id"] = "628xxx"
            jsonRes["messages"][0]["id"] = "xxx"
        
    
        logger.info("Response from Meta : {}".format(jsonRes))
    except Exception as e:
        logger.error("{}".format(e))
        statusCode = 500
        content = {"errorCode": f"{response.status_code}", "errorMessage":"Something went wrong!", "status": "Failed"}
    logger.info("Process Finised. Response payload : {}".format(content))
    
    return JSONResponse(content=content, status_code=statusCode)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)