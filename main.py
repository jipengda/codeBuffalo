import time
import sys
import gi
import graphene
import requests

from enum import Enum
from graphene import ObjectType, String, Field
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk

class Values(ObjectType):
   type = String()
   minAccessibility = String()
   maxAccessibility = String()
   minPrice = String()
   maxPrice = String()
   participants = String()

def extract(url):
    html = requests.get(url).text
    extracted = extraction.Extractor().extract(html, source_url=url)
    return extracted
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

v = Values(type = '',
    minAccessibility = '0.0',
    maxAccessibility = '1.0',
    minPrice = '0.0',
    maxPrice = '1.0',
    participants = ''
    )

class Idea(ObjectType):
    activity = String()
    accessibility = String()
    type = String()
    price = String()
    participants = String()
    link = String()
    key = String()
    name = String()


    @staticmethod
    def getIdea():
        
        query_string = 'http://www.boredapi.com/api/activity?'
        if v.participants != '':  query_string += 'participants=' + v.participants + '&'
        if v.type != '': query_string += 'type=' +v.type + '&'
        if v.minAccessibility == '': v.minAccessibility = '0.0'
        if v.maxAccessibility == '': v.maxAccessibility = '1.0'
        if v.minPrice == '': v.minPrice = '0.0'
        if v.maxPrice == '': v.maxPrice = '1.0'
        query_string += 'minaccessibility=' + v.minAccessibility + '&maxaccessibility=' + v.maxAccessibility + '&minPrice='+v.minPrice+'&maxPrice=' +v.maxPrice 
        
        #in case the user and participant is not selected
        query_string.replace('&&','&')
        print(query_string)
        return requests.get(query_string)



class Query(ObjectType):
    idea = graphene.Field(Idea, url=graphene.String())
    def resolve_idea(self, info):

        r = Idea.getIdea()

        return Idea(activity = r.json()['activity'],
                    key = r.json()['key'],
                    accessibility = r.json()['accessibility'],
                    participants = r.json()['participants'],
                    price = r.json()['price'],
                    type = r.json()['type'],
                    link = r.json()['link']
                    )

class Main:
    def __init__(self):
        gladeFile = "1.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)
        #button = self.builder.get_object("button") 
        #button.connect("clicked", self.printText)
        
        window = self.builder.get_object("Main")
        
        window.connect("delete-event", gtk.main_quit)
        window.show()


    def on_button_clicked(self, b):
        text = self.builder.get_object("text")
        query_string = "{idea {activity type participants price link key accessibility}}"
        schema = graphene.Schema(query=Query)
        result = schema.execute(query_string)
        text.set_text('Activity you should do : ' + result.data['idea']['activity']);

    def on_final_clicked(self, b):
        text = self.builder.get_object("label2")
        p1 = self.builder.get_object("price1")
        p2 = self.builder.get_object("price2")
        a1 = self.builder.get_object("access1")
        a2 = self.builder.get_object("access2")
        e = self.builder.get_object("comboentry")
        s = self.builder.get_object("spin1")

        v.type= e.get_text().lower()
        v.minAccessibility = a1.get_text()
        v.maxAccessibility = a2.get_text()
        v.minPrice = p1.get_text()
        v.maxPrice = p2.get_text()
        v.participants = str(int(s.get_value ()))
        
        try:
            query_string = "{idea {activity type participants price link key accessibility}}"
            schema = graphene.Schema(query=Query)
            result = schema.execute(query_string)
            print(result.data['idea'])
            b = 'activity: ' + result.data['idea']['activity'] + '\n type: ' + result.data['idea']['type'] + '\n participants: ' + result.data['idea']['participants'] + '\n accessibility: ' + result.data['idea']['accessibility'] + '\n price: ' + result.data['idea']['price'] + '\nkey: ' + result.data['idea']['key']
            text.set_text(str(b))
        except:
            text.set_text("There are no acitivities with these parameters. Please choose something else!!")
# print('activity: ' + result.data['idea']['activity'])
# print('type: ' + result.data['idea']['type'])
# print('participants: ' + result.data['idea']['participants'])
# print('price: ' + result.data['idea']['price'])
# print()
# print('accessibility: ' + result.data['idea']['accessibility'])
# print()


    def on_entry1_changed(self, a):
        text = self.builder.get_object("text")
        text.set_text(a.get_text());


    # def on_spin1_value_changed(self, a):
    #     text = self.builder.get_object("text")
    #     b = a.get_value ()
    #     print(b)
    #     text.set_text(str(b));        

    




if __name__ == '__main__':
    mai = Main()
    #mai.show_all()

    gtk.main()