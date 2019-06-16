# This script is going to give you a good activity suggestion based on answers to several questions
# In order to run this script, you need use Python 3.7 or newer version
# You need to pip necessary library to run this file, such as graphene, requests and so on
# You need to input reasonable answer to get the right suggestion
# If you fail to get the activity suggestion, make changes with your answer until you get one
# Have fun with Q&A process!

import graphene
import requests

from enum import Enum
from graphene import ObjectType, String

def Query_find():
    basic = "http://www.boredapi.com/api/activity"
    print("Do you know key number?")
    flag = int(input())
    if flag == 1:
        print("You said yes, please enter a number(1000000,9999999):")
        keyNumber = input()
        Query = basic + '?key=' + keyNumber
    else:
        print("You said no, then do you have a given type?")
        flag = int(input())
        if flag == 1:
            print(
                "You said yes, then please enter a number(1 for education, 2 for recreational, 3 for social, 4 for diy, 5 for charity, 6 for cooking, 7 for relaxation, 8 for music or 9 for busywork)")
            giventype = int(input())
            if giventype == 1:
                add = 'education'
            elif giventype == 2:
                add = 'recreational'
            elif giventype == 3:
                add = 'social'
            elif giventype == 4:
                add = 'diy'
            elif giventype == 5:
                add = 'charity'
            elif giventype == 6:
                add = 'cooking'
            elif giventype == 7:
                add = 'relaxation'
            elif giventype == 8:
                add = 'music'
            else:
                add = 'busywork'
            Query = basic + '?type=' + add
        else:
            print("You said no, then do you know participants number?")
            flag = int(input())
            if flag == 1:
                print("You said yes, then please enter participants number(0,n):")
                number = input()
                Query = basic + '?participants=' + number
            else:
                print("You said no, then do you know specified price?")
                flag = int(input())
                if flag == 1:
                    print("You said yes, then please enter specified price[0,1]:")
                    price = input()
                    Query = basic + '?price=' + price
                else:
                    print("You said no, do you know minprice and maxprice?")
                    flag = int(input())
                    if flag == 1:
                        print("You said yes, then please enter in order minprice and maxprice([0, 1])")
                        minprice = input()
                        maxprice = input()
                        Query = basic + '?minprice=' + minprice + '&' + 'maxprice=' + maxprice
                    else:
                        print("You said no,do you know accessibility number?")
                        flag = int(input())
                        if flag == 1:
                            print("You said yes, then please enter accessibility number[0.0, 1.0]")
                            number = input()
                            Query = basic + '?accessibility=' + number
                        else:
                            print("You said no, do you know minaccessibility and maxaccessibility?")
                            flag = int(input())
                            if flag == 1:
                                print(
                                    "You said yes, then please enter in order minaccessbility and maxaccessbility([0.0, 1.0]):")
                                mina = input()
                                maxa = input()
                                Query = basic + '?minaccessibility=' + mina + '&' + 'maxaccessibility=' + maxa
                            else:
                                Query = basic + '/'
    return Query


def Activity_find(Query_address):
    class ActivityType(Enum):
        EDUCATION = 1
        RECREATIONAL = 2
        SOCIAL = 3
        DIY = 4
        CHARITY = 5
        COOKING = 6
        RELAXATION = 7
        MUSIC = 8
        BUSYWORK = 9

    class Idea(ObjectType):
        activity = String()
        accessibility = String()
        type = String()
        price = String()
        participants = String()
        link = String()
        key = String()
        name = String()

    class Query(ObjectType):
        idea = graphene.Field(Idea, url=graphene.String())

        def resolve_idea(self, info):
            r = requests.get(Query_address)
            return Idea(activity=r.json()['activity'],
                        key=r.json()['key'],
                        accessibility=r.json()['accessibility'],
                        participants=r.json()['participants'],
                        price=r.json()['price'],
                        type=r.json()['type'],
                        link=r.json()['link']
                        )

    query_string = "{idea {activity type participants price link key accessibility}}"
    schema = graphene.Schema(query=Query)
    result = schema.execute(query_string)
    # print("Query_address is " + Query_address)
    print("Excellent! After good consideration, you are suggest do as following: ")
    print('activity: ' + result.data['idea']['activity'])
    print('type: ' + result.data['idea']['type'])
    print('participants: ' + result.data['idea']['participants'])
    print('price: ' + result.data['idea']['price'])
    print('link: ' + result.data['idea']['link'])
    print('accessibility: ' + result.data['idea']['accessibility'])
    print('key: ' + result.data['idea']['key'])


print("Hi Fresh bird, I am going to give you a smart decision when you feel boring, try it out until you get the answer!")
print("1 means Yes, 0 means No")
errorinfo = '{"error":"No activities found with the specified parameters"}'
while(1 == 1):
    Query_address = Query_find()
    detectinfo = requests.get(Query_address)
    info = detectinfo.text
    if info == errorinfo:
        print("Oops! No activities found at this point, please change your answers to get the right activity:)")
    else:
        Activity_find(Query_address)
        break