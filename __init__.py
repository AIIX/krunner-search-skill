"""
Krunner Search Mycroft Skill.
"""

import sys
import re
import operator
from os.path import dirname
from traceback import print_exc
import dbus
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger

__author__ = 'aix'

LOGGER = getLogger(__name__)


class KrunnerPlasmaDesktopSkill(MycroftSkill):
    """
    Krunner Skill Class.
    """

    def __init__(self):
        """
        Krunner Skill Class.
        """
        super(KrunnerPlasmaDesktopSkill, self).__init__(
            name="KrunnerPlasmaDesktopSkill")

    @intent_handler(IntentBuilder("KrunnerKeywordIntent").
                    require("KrunnerPlasmaDesktopSkillKeyword").build())
    def handle_krunner_plasma_desktopskill_intent(self, message):
        """
        Krunner Search By Keyword
        """
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(message.data.get('KrunnerPlasmaDesktopSkillKeyword'), '')
        searchString = utterance

        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.kde.krunner", "/App")
        remote_object.query(
                searchString + ' ', dbus_interface="org.kde.krunner.App")
        self.speak_dialog("krunner.search", data={'Query': searchString})

    @intent_handler(IntentBuilder("RecentFilesIntent").
                    require("RecentFileKeyword").build())
    def handle_krunner_plasma_recentskill_intent(self, message):
        """
        Krunner Search Show Recent
        """
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.kde.krunner", "/App")
        remote_object.query(
            'recent' + ' ', dbus_interface="org.kde.krunner.App")

        self.speak_dialog("krunner.recent")

    @intent_handler(IntentBuilder("CalculateIntent").
                    require("CalculateKeyword").build())
    def handle_krunner_plasma_calculateskill_intent(self, message):
        """
        Krunner Search Calculate
        """
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(message.data.get('CalculateKeyword'), '')
        searchString = utterance
        numbers = [int(x) for x in re.split(
            'minus|-|plus|\+|times|\*|divided by|/|multiply by|multiply|add|subtract|divide by', searchString)]
        operations = re.findall(
            '(minus|-|plus|\+|times|\*|divided by|/|multiply by|multiply|add|subtract|divide by)', searchString)

        if operations[0] == "plus" or operations[0] == "+":
            cal = (str(numbers[0]) + "+" + str(numbers[1]))
            self.sendcalc(cal)
            res = operator.add(numbers[0], numbers[1])
            self.speak("The answer is " + str(res))
        elif operations[0] == "minus" or operations[0] == "-":
            cal = (str(numbers[0]) + "-" + str(numbers[1]))
            res = operator.sub(numbers[0], numbers[1])
            self.speak("The answer is " + str(res))
        elif operations[0] == "times" or operations[0] == "*":
            cal = (str(numbers[0]) + "*" + str(numbers[1]))
            self.sendcalc(cal)
            res = operator.mul(numbers[0], numbers[1])
            self.speak("The answer is " + str(res))
        elif operations[0] == "divided by" or operations[0] == "/":
            cal = (str(numbers[0]) + "/" + str(numbers[1]))
            self.sendcalc(cal)
            res = operator.truediv(numbers[0], numbers[1])
            self.speak("The answer is " + str(res))
        else:
            self.speak("Math operation not found. Supported operations are plus, minus, times or divided by")

    def sendcalc(self, cal):
        """
        Send To Dbus
        """
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.kde.krunner", "/App")
        remote_object.query(
            cal + ' ', dbus_interface="org.kde.krunner.App")

    def stop(self):
        """
        Mycroft Stop Function
        """
        pass


def create_skill():
    """
    Mycroft Create Skill Function
    """
    return KrunnerPlasmaDesktopSkill()
