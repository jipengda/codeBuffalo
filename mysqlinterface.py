import mysql.connector

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

    


