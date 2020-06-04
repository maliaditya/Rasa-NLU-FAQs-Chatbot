# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import sqlite3

con = sqlite3.connect('/home/aditya/Documents/mybot/chatbot/chat_admin/src/chatadmin/db.sqlite3')

cursorObj = con.cursor()


class Actionname(Action):

    def name(self) -> Text:
        return "action_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            name = tracker.latest_message.get('text')
            dispatcher.utter_message(text="How can i help you {}?".format(name))
     
            return []
            
class ActionDefaultFallback(Action):
    
   def name(self):
      return "action_default_fallback"

   def run(self, dispatcher, tracker, domain):
       quest = tracker.latest_message.get('text')
       que1 = "INSERT INTO home_quetions( question )  VALUES ('%s' )" %  (quest)   
       cursorObj.execute(que1)
       con.commit() 
       dispatcher.utter_message("Sorry, I couldn't understand.")








class ActionFormInfo(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
     

        return ["name_er","surname","age","GENDER","GRADE","phone",]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template

        dispatcher.utter_message(template="utter_submit", name=tracker.get_slot('age'),
                                 GRADE=tracker.get_slot('GRADE'), name_get=tracker.get_slot('name_er'))

        dispatcher.utter_message(text = "https://goo.gl/maps/Z5ZZKJ5ehLWNkCGV7")
        

        name = tracker.get_slot('name_er')
        age = tracker.get_slot('age')
        gender = tracker.get_slot('GENDER')
        grade = tracker.get_slot('GRADE')
        phone = tracker.get_slot('phone')
        surname = tracker.get_slot('surname')

        que = "INSERT INTO home_lead( name,surname, age, gender,grade,phone)  VALUES ('%s','%s','%s', '%s', '%s','%s' )" %  (name, surname, age, gender, grade, phone)    
        cursorObj.execute(que)
        con.commit()
        que = "INSERT INTO home_lead( name,surname, age, gender,grade,phone)  VALUES ('%s','%s','%s', '%s', '%s','%s' )" %  (name, surname, age, gender, grade, phone)    


        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [self.from_entity(entity="age", intent="for_age"),
                     self.from_text()],
            "GRADE": [self.from_entity(entity="GRADE", intent="For_grade"),
                        self.from_text()],
            "Gender": [self.from_entity(entity="GENDER", intent="gender"),
                        self.from_text()],
        }


