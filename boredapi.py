class Query(graphene.ObjectType):
  r = requests.get('http://www.boredapi.com/api/activity/')
  #myactivity = 
  print(r.json()['participants'])
  myactivity = graphene.String(activity=graphene.String(default_value=(r.json()['activity'])))

  def resolve_myactivity(self, info, activity):
    return 'activity: ' + activity

schema = graphene.Schema(query=Query)
result = schema.execute('{ myactivity }')
print(result.data['myactivity']) # "Hello World"
