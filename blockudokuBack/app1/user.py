import traceback
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from blockudokuBack.settings import *
from django.db import connection
import pytz
import datetime

# ene debug uyed ajillah yostoi
def userListView(request):
    print("ffff")
    myCon = connectDB()
    userCursor = myCon.cursor()
    userCursor.execute('SELECT * FROM "t_user" ORDER BY id ASC')
    columns = userCursor.description
    response = [{columns[index][0]: column for index,
                 column in enumerate(value)} for value in userCursor.fetchall()]
    userCursor.close()
    disconnectDB(myCon)
    for item in response:
        if 'created_at' in item:
            item['created_at'] = item['created_at'].astimezone(
                pytz.utc).replace(tzinfo=None)
    responseJSON = json.dumps(response, cls=DjangoJSONEncoder, default=str)
    return HttpResponse(responseJSON, content_type="application/json")
#   userListView

def userLoginView(request):
    jsons = json.loads(request.body)
    if (reqValidation(jsons, {"name", "pass", }) == False):
        resp = {}
        resp["responseCode"] = 550
        resp["responseText"] = "Field-үүд дутуу"
        return HttpResponse(json.dumps(resp), content_type="application/json")
    myName = jsons['name']
    myPass = jsons['pass']
    try:
        myCon = connectDB()
        userCursor = myCon.cursor()
        userCursor.execute("SELECT \"id\",\"name\",\"email\" "
                           " FROM t_user"
                           " WHERE "
                           " deldate IS NULL AND "
                           " pass = %s AND "
                           " \"userName\" = %s ",
                           (
                               myPass,
                               myName,
                           ))
        columns = userCursor.description
        response = [{columns[index][0]: column for index, column in enumerate(
            value)} for value in userCursor.fetchall()]
        userCursor.close()
    except Exception as e:
        resp = {}
        resp["responseCode"] = 551
        resp["responseText"] = "Баазын алдаа"
        return HttpResponse(json.dumps(resp), content_type="application/json")
    finally:
        disconnectDB(myCon)
    responseCode = 521  # login error
    responseText = 'Буруу нэр/нууц үг'
    responseData = []

    if len(response) > 0:
        responseCode = 200
        responseText = 'Зөв нэр/нууц үг байна хөгшөөн'
        responseData = response[0]
    resp = {}
    resp["responseCode"] = responseCode
    resp["responseText"] = responseText
    resp["userData"] = responseData
    resp["Сургууль"] = {}
    resp["Сургууль"]["Нэр"] = "Мандах"
    resp["Сургууль"]["Хаяг"] = "3-р хороолол"

    return HttpResponse(json.dumps(resp), content_type="application/json")

#   userLoginView end#########################################################
def userRegisterView(request):
    jsons = json.loads(request.body)
    # Validate request body
    if reqValidation(jsons, {"firstName", "lastName", "email", "pass", "userName"}) == False:
        resp = {
            "responseCode": 550,
            "responseText": "Field-үүд дутуу"
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")
    firstName = jsons['firstName']
    lastName = jsons['lastName']
    email = jsons['email']
    password = jsons['pass']
    username = jsons['userName']
    try:
        myCon = connectDB()
        userCursor = myCon.cursor()

        if emailExists(email):
            resp = {
                "responseCode": 400,
                "responseText": "Бүртгэлтэй email байна."
            }
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if userNameExists(username):
            resp = {
                "responseCode": 400,
                "responseText": "Бүртгэлтэй хэрэглэгчийн нэр байна."
            }
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if not myCon:
            raise Exception("Can not connect to the database")
    except Exception as e:
        resp = {
            "responseCode": 551,
            "responseText": "Баазын алдаа"
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")
    userCursor.execute(
        'INSERT INTO "f_user"("firstName", "lastName", "email", "pass", "userName", "deldate", "usertypeid") '
        'VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING "id"',
        (firstName, lastName, email, password, username, None, 2,))
    userId = userCursor.fetchone()[0]
    # Add user ID to other tables
    current_date = datetime.date.today()
    date = current_date.strftime("%m/%d/%Y")
    userCursor.execute(
        'INSERT INTO "f_userNemeltMedeelel"("user_id", "huis", "torsonOgnoo") VALUES(%s,%s,%s)',
        (userId,1,date))
    myCon.commit()
    # Close the userCursor and disconnect from the database
    userCursor.close()
    disconnectDB(myCon)

    # Return success response
    resp = {
        "responseCode": 200,
        "responseText": "Амжилттай бүртгэгдлээ"
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")
######################################################################################