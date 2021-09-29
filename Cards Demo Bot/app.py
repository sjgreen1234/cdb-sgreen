from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
from cardcontent import *
import smartsheet

app = Flask(__name__)
api = WebexTeamsAPI(access_token="OTI2OTcyODEtNzk2Yy00NWU5LWFhOTEtNTNiYmU5MzE4YTEyNTRjMjE3NzUtMGM3_PF84_cca99e60-7e42-4fa8-ab73-90635eb378a6")

@app.route('/', methods=['POST', 'GET'])
def home(): 
    return 'OK', 200

@app.route('/webhookreq', methods=['POST', 'GET'])
def webhookreq():
    if request.method == 'POST':
        req = request.get_json()

        data_personId = req['data']['personId']
        data_roomId = req['data']['roomId']

        #Loop prevention VERY IMPORTNAT! 
        me = api.people.me() 
        if data_personId == me.id: 
            return 'OK', 200 
        else: 
            if api.messages.create(roomId=data_roomId, text='Hello World!!!' , attachments=[{"contentType": "application/vnd.microsoft.card.adaptive", "content": cardcontent}]):
                return "OK" 
        
    elif request.method == 'GET': 
        return "Yes, this is working."
    return 'OK', 200

@app.route('/cardsubmitted', methods=['POST'])
def cardsubmitted():
    if request.method == 'POST':
        req = request.get_json()

        data_id = req['data']['id']

        attachment_actions = api.attachment_actions.get(data_id)
        inputs = attachment_actions.inputs

        myName = inputs['myName']
        myEmail = inputs['myEmail']
        myTel = inputs['myTel']

        print(myName)
        print(myEmail)
        print(myTel)

        smart = smartsheet.Smartsheet('Vcq5CNOdxWH0YkE9WCJPaK9qa9vdfLzDtTmY2') #Smartsheet Access Token
        smart.errors_as_exceptions(True)

        # Specify cell values for the added row                         
        newRow = smartsheet.models.Row()
        newRow.to_top = True
      # The above variables are the incoming JSON
        newRow.cells.append({ 'column_id': 1959328226797444, 'value': myName })                   #  
        newRow.cells.append({ 'column_id': 4211128040482692, 'value': myEmail, 'strict': False })   
        newRow.cells.append({ 'column_id': 551953343244164, 'value': myTel, 'strict': False }) 
        response = smart.Sheets.add_rows(1872658196391812, newRow) # The -- xxxxxxxxxxxxxx -- on this line is the sheet ID.
    return 'OK', 200
     
if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0")
