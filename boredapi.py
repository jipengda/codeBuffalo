import graphene
import requests
from enum import Enum

from graphene import ObjectType, String, Field

def extract(url):
    html = requests.get(url).text
    extracted = extraction.Extractor().extract(html, source_url=url)
    return extracted

class ActivityType(Enum):
  EDUCATION = 1
  RECREATIONAL =2 
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
    name=String()




class Query(ObjectType):
  
  idea = graphene.Field(Idea, url = graphene.String())

  def resolve_idea(self, info):
        r = requests.get('http://www.boredapi.com/api/activity/')
        return Idea(activity = r.json()['activity'],
                    key = r.json()['key'],
                    accessibility = r.json()['accessibility'],
                    participants = r.json()['participants'],
                    price = r.json()['price'],
                    type = r.json()['type'],
                    link = r.json()['link']
                    )

query_string = "{idea {activity type participants price link key accessibility}}"

schema = graphene.Schema(query=Query)
result = schema.execute(query_string)
print('activity: ' + result.data['idea']['activity'])
print('type: ' + result.data['idea']['type'])
print('participants: ' + result.data['idea']['participants'])
print('price: ' + result.data['idea']['price'])
print('link: ' + result.data['idea']['link'])
print('accessibility: ' + result.data['idea']['accessibility'])
print('key: ' + result.data['idea']['key'])

