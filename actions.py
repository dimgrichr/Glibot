# This files contains your custom actions which can be used to run
# custom Python code.


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector




class GetSchedule(Action):
    def name(self) -> Text:
        return "action_get_schedule"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        schedule_type = next(tracker.get_latest_entity_values('schedule'), None)
        if schedule_type is not None:
            dispatcher.utter_message("Θα βρείτε το {}".format(schedule_type)+" στον παρακάτω σύνδεσμο: \n https://ihst.csd.auth.gr/courses-exams-schedule/")
        else:
            dispatcher.utter_message("Θα βρείτε τα προγράμματα μαθημάτων και εξετάσεων στον παρακάτω σύνδεσμο: \n https://ihst.csd.auth.gr/courses-exams-schedule/")
        return []



class GetContact(Action):
    def name(self) -> Text:
        return "action_get_contact"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mydb = mysql.connector.connect(user='bot', 
                                       password='bot',
                                       host='localhost',
                                       database='Chatbot')
        mycursor = mydb.cursor()
        contact_type = next(tracker.get_latest_entity_values('contact'), None)
        mycursor.execute("SELECT Value FROM Contact")
        myresult = mycursor.fetchall()
        list(myresult)

        if str(contact_type) == 'αριθμός επικοινωνίας':
            strg = 'Επικοινωνήστε με την γραμματεία τηλεφωνικά, στον αριθμό: ' + str(myresult[0])[2:12]
        elif str(contact_type) == 'email':
            strg = 'Επικοινωνήστε με την γραμματεία μέσω email, στην διεύθυνση: ' + str(myresult[1])[2:22]
        elif str(contact_type) == 'fax':
            strg = 'Επικοινωνήστε με την γραμματεία μέσω fax, στoν αριθμό: ' + str(myresult[2])[2:12]
        else:
            strg = 'Επικοινωνήστε με την γραμματεία: \n 1)Τηλεφωνικά, στον αριθμό: ' + str(myresult[0])[2:12] + ' \n2)Με email, στην διεύθυνση:' + str(myresult[1])[2:22] + '\n3)Με fax, στον αριθμό:' + str(myresult[2])[2:12]
        dispatcher.utter_message(strg)
        mydb.close()        
        return []



class InfoAboutCourse(Action):
    def name(self) -> Text:
        return "action_get_info_about_course"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mydb = mysql.connector.connect(user='bot', 
                                       password='bot',
                                       host='localhost',
                                       database='Chatbot')
        mycursor = mydb.cursor()
        semester_type = next(tracker.get_latest_entity_values('semester'), None)
        course_type = next(tracker.get_latest_entity_values('course_type'), None)
        prof = next(tracker.get_latest_entity_values('prof'), None)
        if semester_type is None: 
            if course_type is None: 
                mycursor.execute("SELECT * FROM Courses")
            elif str(course_type) == 'Υ':
                mycursor.execute("SELECT * FROM Courses WHERE Type='Υ'")
            elif str(course_type) == 'ΠΠ':
                mycursor.execute("SELECT * FROM Courses WHERE Type='ΠΠ'")
            else:
                mycursor.execute("SELECT * FROM Courses WHERE Type='Ε' OR Type='ΥΕ'")
        elif str(semester_type) == '1ου':
            mycursor.execute("SELECT * FROM Courses WHERE Semester='1'")
        else:
            mycursor.execute("SELECT * FROM Courses WHERE Semester='2'")
        myresult = mycursor.fetchall()
        strg = ''
        if prof is None:
            for Name, id, Professors, Subject, Weekly, Type, ECTS, Semester in myresult:
                strg += 'Όνομα: ' + str(Name) + '  Id: ' + str(id) + '  Καθηγητές: ' + str(Professors) + '  Ώρες Εβδομαδιαίως: ' + str(Weekly) + '   Τύπος: ' + str(Type) + '  ECTS: ' + str(ECTS) + '  Εξάμηνο: ' + str(Semester) + '\n'
        else:
            strg +='Τα μαθήματα που διδάσκει ο ' + str(prof) +' είναι τα εξής: \n'
            for Name, id, Professors, Subject, Weekly, Type, ECTS, Semester in myresult:
                if str(prof) in str(Professors):
                    strg += 'Όνομα: ' + str(Name) + '  Id: ' + str(id) + '  Καθηγητές: ' + str(Professors) + '  Ώρες Εβδομαδιαίως: ' + str(Weekly) + '   Τύπος: ' + str(Type) + '  ECTS: ' + str(ECTS) + '  Εξάμηνο: ' + str(Semester) + '\n'

        dispatcher.utter_message(strg)
        mydb.close()        
        return []


class InfoAboutLocations(Action):
    def name(self) ->Text:
        return "action_get_info_about_locations"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        strg = ''
        mydb = mysql.connector.connect(user='bot', 
                                       password='bot',
                                       host='localhost',
                                       database='Chatbot')
        mycursor = mydb.cursor()
        loc = next(tracker.get_latest_entity_values('amphitheatre'), None)
        if loc is None:
            mycursor.execute("SELECT * FROM Amphitheatres")
            myresult = mycursor.fetchall()
            strg += "Οι διαθέσιμες αίθουσες, στις οποίες πραγματοποιούνται διαλέξεις, είναι οι εξής: \n"
            for Name, Location in myresult:
                strg += 'Αίθουσα ' + str(Name) + '    Τοποθεσία: ' + str(Location) + "\n"
            strg += "\n" + 'H τοποθεσία του Παραρτήματος της Πληροφορικής ΑΠΘ :  https://goo.gl/maps/voV84hZVfkU7AS7R7'
            strg += "\n" + 'Η τοποθεσία του Ημιωρόφου της Πληροφορικής του ΑΠΘ:  https://goo.gl/maps/fJTsaiishxq6nzpZ8'
        elif str(loc) == 'ΕΑ3':
            mycursor.execute("SELECT Location FROM Amphitheatres WHERE Name='ΕΑ3'")
            myresult = mycursor.fetchall()
            strg = 'Η αίθουσα ΕΑ3, βρίσκεται στην τοποθεσία: '
            for Location in myresult:
                strg += str(Location)[2:44] + "\n"
            strg += "\n" + 'H τοποθεσία του Παραρτήματος της Πληροφορικής ΑΠΘ :  https://goo.gl/maps/voV84hZVfkU7AS7R7'
        elif str(loc) == 'ΕΑ4':
            mycursor.execute("SELECT Location FROM Amphitheatres WHERE Name='ΕΑ4'")
            myresult = mycursor.fetchall()
            strg = 'Η αίθουσα ΕΑ4, βρίσκεται στην τοποθεσία: '
            for Location in myresult:
                strg += str(Location)[2:44] + "\n"
            strg += "\n" + 'H τοποθεσία του Παραρτήματος της Πληροφορικής ΑΠΘ :  https://goo.gl/maps/voV84hZVfkU7AS7R7'
        else:
            mycursor.execute("SELECT Location FROM Amphitheatres WHERE Name='Η3'")
            myresult = mycursor.fetchall()
            strg = 'Η αίθουσα Η3, βρίσκεται στην τοποθεσία: '
            for Location in myresult:
                strg += str(Location)[2:28] + "\n"
            strg += "\n" + 'Η τοποθεσία του Ημιωρόφου της Πληροφορικής του ΑΠΘ:  https://goo.gl/maps/fJTsaiishxq6nzpZ8'

        dispatcher.utter_message(strg)
        mydb.close()        
        return []


class Fallback(Action):
    def name(self) -> Text:
        return "action_fallback"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            dispatcher.utter_message("Δεν αντιλαμβάνομαι τι εννοείς.")
            return []

















