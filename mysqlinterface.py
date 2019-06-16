import mysql.connector
import graphene

class databaseConnection:
    def __init__(self, user, password, host, database):
        self.connection = mysql.connector.connect(user=user,
                password=password, host=host,
                database=database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def addOrGetAttribute(self, attribute):
        self.cursor.execute(
        f"SELECT attribute_id FROM activity_attribute WHERE attribute_text = '{attribute}'")
        result = list(self.cursor)
        if not result:
            self.cursor.execute(
            f"INSERT INTO activity_attribute (attribute_text) VALUES ('{attribute}');")
            self.connection.commit()
            self.cursor.execute('SELECT LAST_INSERT_ID();')
            result = list(self.cursor)
        return result[0][0]

    def setAttribute(self, activity_key, attribute_id, truth):
        self.cursor.execute(
        f"SELECT COUNT(*) FROM activity_attribute_ref WHERE activity_key = {activity_key} and attribute_id = {attribute_id}")
        if list(self.cursor)[0][0] == 0:
            self.cursor.execute(
            f"INSERT INTO activity_attribute_ref (activity_key, attribute_id, activity_has_attribute) VALUES ({activity_key}, {attribute_id}, {truth})")
        else:
            self.cursor.execute(
            f"UPDATE activity_attribute_ref SET activity_has_attribute = {truth} WHERE activity_key = {activity_key} AND attribute_id = {attribute_id}")
        self.connection.commit()
    
    def checkAttribute(self, activity_key, attribute):
        attribute_id = self.addOrGetAttribute(attribute)
        self.cursor.execute(
        f"SELECT activity_has_attribute FROM activity_attribute_ref WHERE activity_key = {activity_key} AND attribute_id = {attribute_id}")
        result = list(self.cursor)
        if not result:
            return None
        return result[0][0] != 0

class Opinion(graphene.ObjectType):
    attribute = graphene.String()
    ideaKey = graphene.String()
    hasOpinion = graphene.Boolean()
    opinionValue = graphene.Boolean()

class QueryOpinion(graphene.ObjectType):
    opinion = graphene.Field(Opinion)
    def resolve_opinion(self, info):
        idea_key = info.context['idea_key']
        attribute = info.context['attribute']
        mysqlLink = databaseConnection('team32_user', 'bron is life', '35.238.128.54', 'team32_db') # TODO: un-hardcode credentials
        result = mysqlLink.checkAttribute(int(idea_key), attribute)
        del mysqlLink
        has_opinion = result is not None
        opinion_value = result == 1
        return Opinion(attribute = attribute,
                ideaKey = idea_key,
                hasOpinion = has_opinion,
                opinionValue = opinion_value)

class MutateOpinion(graphene.Mutation):
    class Arguments:
        ideaKey = graphene.String()
        attribute = graphene.String()
        opinionValue = graphene.Boolean()

    ok = graphene.Boolean()

    def mutate(root, info, ideaKey, attribute, opinionValue):
        mysqlLink = databaseConnection('team32_user', 'bron is life', '35.238.128.54', 'team32_db') # TODO: un-hardcode credentials
        attribute_id = mysqlLink.addOrGetAttribute(attribute)
        mysqlLink.setAttribute(int(ideaKey), attribute_id, opinionValue)
        del mysqlLink
        opinion = Opinion(attribute = attribute,
                ideaKey = ideaKey,
                hasOpinion = True,
                opinionValue = opinionValue)
        ok = True
        return MutateOpinion(ok=ok)
        
class Mutation(graphene.ObjectType):
    mutate_opinion = MutateOpinion.Field()


