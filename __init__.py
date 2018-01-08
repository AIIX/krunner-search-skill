import sys
import dbus
import re
from traceback import print_exc
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'aix'

LOGGER = getLogger(__name__)


class KrunnerPlasmaDesktopSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(KrunnerPlasmaDesktopSkill, self).__init__(name="KrunnerPlasmaDesktopSkill")
        
    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        krunner_plasma_desktopskill_intent = IntentBuilder("KrunnerKeywordIntent").\
            require("KrunnerPlasmaDesktopSkillKeyword").build()
        self.register_intent(krunner_plasma_desktopskill_intent, self.handle_krunner_plasma_desktopskill_intent)
        
        krunner_plasma_recentskill_intent = IntentBuilder("RecentFilesIntent").\
            require("RecentFileKeyword").build()
        self.register_intent(krunner_plasma_recentskill_intent, self.handle_krunner_plasma_recentskill_intent)
        
        krunner_plasma_calculateskill_intent = IntentBuilder("CalculateIntent").\
            require("CalculateKeyword").build()
        self.register_intent(krunner_plasma_calculateskill_intent, self.handle_krunner_plasma_calculateskill_intent)

    def handle_krunner_plasma_desktopskill_intent(self, message):
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(
                message.data.get('KrunnerPlasmaDesktopSkillKeyword'), '')
        searchString = utterance
        
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.kde.krunner","/App") 
        remote_object.query(searchString + ' ', dbus_interface = "org.kde.krunner.App")
        
        self.speak_dialog("krunner.search", data={'Query': searchString})

    
    def handle_krunner_plasma_recentskill_intent(self, message):        
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.kde.krunner","/App") 
        remote_object.query('recent' + ' ', dbus_interface = "org.kde.krunner.App")
        
        self.speak_dialog("krunner.recent")
        
    def handle_krunner_plasma_calculateskill_intent(self, message):
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(
                message.data.get('CalculateKeyword'), '')
        searchString = utterance
        numbers = [int(x) for x in re.split('minus|plus|times|divided by|multiply by|multiply|add|subtract|divide by', searchString)]
        operations = re.findall('(minus|plus|times|divided by|multiply by|multiply|add|subtract|divide by)', searchString)
        if operations[0] == "plus" or "add":
            cal = (str(numbers[0]) + "+" + str(numbers[1]))
            self.sendcalc(cal)
        elif operations[0] == "minus" or "subtract":
            cal = (str(numbers[0]) + "-" + str(numbers[1]))
            self.sendcalc(cal)
        elif operations[0] == "times" or "multiply" or "multiply by":
            cal = (str(numbers[0]) + "*" + str(numbers[1]))
            self.sendcalc(cal)
        elif operations[0] == "divided by" or "divide by":
            cal = (str(numbers[0]) + "/" + str(numbers[1]))
            self.sendcalc(cal)
        else:
            self.speak("Math operation not found supported operations are plus, minus, times or divided by")
        
    def sendcalc(self, cal):
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.kde.krunner","/App") 
        remote_object.query(cal + ' ', dbus_interface = "org.kde.krunner.App")
    
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return KrunnerPlasmaDesktopSkill()
