from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, ActiveLoop, SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from actions.helper import create_button, create_hyper_link, remove_slot_values

# Constants
SOMETHING_IS_WRONG = "Something is Wrong"


# Helper Function
def get_slot_value(tracker: Tracker, slot_name):
    return tracker.slots.get(slot_name)


class ActionPath(Action):
    def name(self) -> Text:
        return "action_path"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [{"title": "I want to ask about family planning.", "payload": "I want to ask about family planning."},
                   {"title": "I want the nearest family planning clinic to me.",
                    "payload": "I want the nearest family planning clinic to me."},
                   {"title": "Other reproductive health issues.", "payload": "Other reproductive health issues."}]
        dispatcher.utter_button_message("What would you like to know about?", buttons)
        return []


class ActionFamilyMethod(Action):

    def name(self) -> Text:
        return "action_family_method"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [{"title": "I want to start using a method.", "payload": " I want to start using a method."},
                   {"title": " I want to start using another method.",
                    "payload": " I want to start using another method."},
                   {"title": "  I want to know about side effects.",
                    "payload": "  I want to know about side effects."},
                   {"title": "  I want to know about family planning products.",
                    "payload": " I want to know about family planning products."}]
        dispatcher.utter_button_message("What would you like to know about?", buttons)
        return []


class ValidateRequestFamilyPlanningUsingMethodForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_request_family_planning_using_method_form"

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()

        print(get_slot_value(tracker, 'is_planned_family_planning_before'))
        if get_slot_value(tracker, 'is_planned_family_planning_before') == "No":
            updated_slots.remove("followed_method_before")
            updated_slots.remove("satisfied_last_method")
            updated_slots.remove("reason_for_not_satisfied")

        if get_slot_value(tracker, 'satisfied_last_method') == 'Yes':
            updated_slots.remove("reason_for_not_satisfied")

        print(f"updated Slots: {updated_slots}")
        return updated_slots


class ActionNextActions(Action):

    def name(self):
        return "action_next_options"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        next_response = {'0-3 months': 'utter_0_3_months_response',
                         '1-2 years': 'utter_1_2_years_response',
                         '3-4 years': 'utter_3_4_years_response',
                         '5-10 years': 'utter_5_10_years_response',
                         '1-2 permanently': 'utter_permanently_response',

                         }

        dispatcher.utter_message(response=next_response.get(get_slot_value(tracker, 'prevent_pregnancy_time'),
                                                            "Invalid Option Selected"))
        return []


# 0_3 Months flow

class AskForSlot03MonthsMethod(Action):
    def name(self) -> Text:
        return "action_ask_0_3_months_method"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        button_details = create_button(["Daily contraceptive pills", "Emergency contraceptive pills",
                                        "Injectable contraceptives", "Diaphragm", "Female condom", "Male condom"])
        dispatcher.utter_message(text="The short-term family planning methods are: \n "
                                      "1. Daily contraceptive pills\n"
                                      "2. Emergency contraceptive pills\n"
                                      "3. The barrier contraceptives which are the diaphragms and "
                                      "condoms and then the Injectables.\n"
                                      "Click on any of them to get the full details about them.",
                                 buttons=button_details)
        return []


class AskForSlotDailyPillsAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_daily_pills_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        audio_link = create_hyper_link(url='https://drive.google.com/file/d/1XLnrE5GF2eW8A8_9uJ0M3IhAzzpu0ijx/view'
                                           '?usp=drive_link',
                                       url_description='Audio embedding (Daily pills)')
        message = "Daily pills are combined oral contraceptive (COC) pills for pregnancy prevention, dermatological " \
                  "and gynecological conditions, and management of menstrual irregularities (heavy bleeding, " \
                  "painful menstruation, premenstrual syndrome). " \
                  "They work by thickening the mucus around the cervix, which makes it difficult for sperm to enter " \
                  "the uterus and reach any eggs that may have been released. " \
                  "Most combination pills come in either a 21-day pack (Dianofem and Desofem) or a 28-day pack (" \
                  "Levofem). One pill is taken each day at about the same time for 21 days. Depending on your pack, " \
                  "you will either have a 7-day break (as in the 21-day pack) or you will take the pill that contains " \
                  "Iron for 7 days (the 28-day pack). \n" \
                  "Click to listen to a short introduction of daily pills in Pidgin, if you want to.\n" \
                  f"{audio_link}\n" \
                  f"Now let me tell you some of the advantages and disadvantages of daily pills.\n" \
                  f"Advantages \n" \
                  f"1. They are very effective if used correctly.\n" \
                  f"2. Very safe for the majority of women.\n" \
                  f"3. Return to fertility is very fast.\n" \
                  f"4. They regularize the menstrual cycle, reduce heavy menstrual flow, and " \
                  f"reduce menstrual and ovulation pain.\n" \
                  f"5. They are simple and easy to use.\n" \
                  f"Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotDailyPillsDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_daily_pills_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now to the disadvantages of daily pills.\n" \
                  "Disadvantages\n" \
                  "1. They must be taken daily which might be difficult to comply with.\n" \
                  "2. They might cause mild and temporary side effect which usually goes away after some weeks such " \
                  "as:\n" \
                  "a. Mild headache.\n" \
                  "b. Nausea or vomiting.\n" \
                  "c. Spotting or bleeding at intervals.\n" \
                  "d. Breast tenderness and soreness to touch.\n" \
                  "e. Mood changes.\n" \
                  "Are you with me?"
        button_details = create_button(["Yes", "No"])
        dispatcher.utter_message(text=message, buttons=button_details)
        return []


class AskForSlotWhoCanAndCannotDailyPills(Action):
    def name(self) -> Text:
        return "action_ask_daily_who_can_use_pills"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "On who can use and who cannot use daily pills.\n Who can use \n" \
                  "1.You can use daily pills if you want a short-term contraceptive method.\n" \
                  "2. If you are a breastfeeding mother (from six months after birth)\n" \
                  "3. If you have irregular menstrual cycle.\n" \
                  "4. If you don't have migrainous headaches.\n" \
                  "5. If you are taking antibiotics, antifungal or antiparasitic medications.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotMedicalConditions(Action):
    def name(self) -> Text:
        return "action_ask_daily_medical_conditions"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Who cannot use\n" \
                  "1. If you are a breastfeeding mother from 6 weeks to 6 months postpartum.\n" \
                  "2. If you are a smoker and over 35 years old.\n" \
                  "3. If you have any of the following medical conditions, it is not advisable to take daily piils:\n" \
                  "a. Blood Pressure\n" \
                  "b. Venous thromboembolism\n" \
                  "c. Stroke.\n" \
                  "d. Heart Disease.\n" \
                  "e. Liver Disease\n" \
                  "f. Breast Cancer\n" \
                  "g. Diabetes\n" \
                  "h. Sickle-cell Anaemia"
        dispatcher.utter_message(text=message)
        message = "Do you have any of the medical conditions listed?"
        buttons = create_button(["Yes", "No", "I don't know"])
        dispatcher.utter_message(text=message, buttons=buttons)
        return []


class AskForSlotDailyContraceptiveDatabase(Action):
    def name(self) -> Text:
        return "action_ask_daily_contraceptive_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Let me tell you some of the effective and available daily contraceptive pills.\n" \
                  "Click on any of them to get their full details."
        buttons = create_button(["Levofem", "Desofem", "Dianofem"])
        dispatcher.utter_message(text=message, buttons=buttons)
        return []


def get_daily_contraceptive_database_message(key_value: str):
    messages = {"Levofem": "Levofem is a safe, low-dose, combined oral contraceptive used to prevent pregnancy. Each "
                           "pack contains 21 active yellow tablets and 7 placebo(inactive) tablets which should be "
                           "taken around the same time daily. How to Use\n"
                           " 1. Take your first pill from the packet "
                           "marked with the correct day of the week, or the first pill of the first colour (phasic "
                           "pills)\n"
                           " 2. Continue to take a pill at the same time each day until the pack is finished. "
                           "Continue taking pills for seven days (during these seven days you will get a bleed).\n"
                           " 3. Start your next pack of pills on the eighth day, whether you are still bleeding or"
                           " not. This should be the same day of the week as when you took your first pill\n"
                           "You can buy Levofem at any pharmacy or health store around you.",
                "Desofem": "Desofem is a safe and effective daily pill used in the treatment of certain menstrual "
                           "disorders as well as to prevent pregnancy. How to Use One pill is taken around the same "
                           "time daily for 21 days followed by a 7-day break, then continue with the next pack.",
                "Dianofem": "Dianofem is a safe and effective pill that contains a combination of an antiandrogen ("
                            "Cyprolerone Acetate 2mg) and estrogen (Ethinylestradiol 0.035mg) used for the treatment "
                            "of dermatological and gynecological conditions in women. It also prevents pregnancy. It "
                            "contains 21 tablets with no placebo (inactive pills). How to Use Take one tablet daily "
                            "for 21 days, followed by a 7-day break where no tablets are taken. Start the next pack "
                            "after the 7-day break."}
    return messages.get(key_value, SOMETHING_IS_WRONG)


# Emergency
class AskForSlotEmergencyPillExplanation(Action):
    def name(self) -> Text:
        return "action_ask_emergency_pill_explanation"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Emergency contraceptive pills are pills taken immediately after unprotected sex to prevent " \
                  "pregnancy. They contain 1.5mg Levonorgestrel and it is a one-dose medication. They work by " \
                  "stopping the release of an egg from your ovary. It may prevent sperm from fertilizing the egg and " \
                  "if fertilization occurs, it may prevent the fertilized egg from attaching to the womb. Emergency " \
                  "pills are very effective when taken before sex especially during ovulation or within 24 to 72 " \
                  "hours after unprotected sex. Please note that they have no effect on already established " \
                  "pregnancy. \n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotEmergencyPillAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_emergency_pill_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now let me tell you some of the advantages and disadvantages of emergency pills. Advantages\n" \
                  "1. Emergency pills are safe for all women including breastfeeding mothers with babies 6 weeks or " \
                  "older.\n" \
                  "2. They are convenient, readily available and easy to use.\n" \
                  "3. The one-dose regimen ensures compliance.\n" \
                  "4. They reduce the need for abortion.\n" \
                  "5.Their side effects are of very short duration.\n" \
                  "6. Quick and easiest option for preventing unplanned pregnancy.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotEmergencyPillDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_emergency_pill_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now to the disadvantages of emergency pills.\n" \
                  " Disadvantages \n" \
                  "1. They must be taken daily within 3 days of unprotected sex.\n" \
                  " 2. They are less effective than regular contraceptives. \n" \
                  "3. They might cause mild and temporary side effect which usually goes away after some days such as: " \
                  "a. Mild headache.\n" \
                  "b. Nausea or vomiting.\n" \
                  "c. Dizziness.\n" \
                  "d. Breast tenderness.\n" \
                  "e. Lower abdominal discomfort.\n" \
                  "f. Menstrual change (period may come early)\n" \
                  "Are you with me?"
        buttons = create_button(["Yes", "No"])
        dispatcher.utter_message(text=message, buttons=buttons)
        return []


class AskForSlotEmergencyWhoCanAndCannotUseContraceptive(Action):
    def name(self) -> Text:
        return "action_ask_emergency_who_can_and_cannot_use_contraceptive"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """On who can use and who cannot use emergency pills.\n
        Who can use\n
        All women can use emergency contraceptive pills safely and effectively, including women who cannot 
        use continuing hormonal contraceptive methods\n. 
        Because of the short-term nature of their use there are no medical conditions that make 
        emergency contraceptive pills unsafe for any woman. 
        Who cannot use\n
        Not suitable for women wth confirmed or suspected pregnancy.\n
        Do you understand?"""
        dispatcher.utter_message(text=message)
        return []


class AskForSlotEmergencyContraceptiveDatabase(Action):
    def name(self) -> Text:
        return "action_ask_emergency_contraceptive_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Let me tell you some of the effective and available daily contraceptive pills. \n" \
                  "Click on any of them to get their full details."
        buttons = create_button(["Postpill", "Postinor 2"])
        dispatcher.utter_message(text=message, buttons=buttons)
        return []


def get_emergency_contraceptive_database_message(key_value: str):
    messages = {"Postpill": "Postpill is a one-dose emergency contraceptive pill by DKT. It contains 1.5 mg "
                            "Levongestrel. POSTPILL should be taken orally as soon as possible within 24 hours but can "
                            "still be taken within 5 days (120 hours) of unprotected\n"
                            "You can click on the audio below to listen to a short introduction of Postpill "
                            "in Pidgin if you want to.\n"
                            f"{create_hyper_link(url='https://drive.google.com/file/d/15O1QpDcxI9Zf1XvoR8REp788YVQcC-Hp/view?usp=drive_link', url_description='Audio embedding (Postpill)')}\n"
                            f"You can buy Postpill at any pharmacy or health store around you.",
                "Postinor 2": "POSTINOR is an Emergency Contraceptive Pill (ECP) that safely prevents unwanted "
                              "accidental pregnancy within 72 hours after unprotected sexual intercourse. "
                              "It doesn’t work if you are already pregnant and will not harm an already established pregnancy. The sooner you take "
                              "POSTINOR, the more effective it is.\n"
                              "You can buy it at any pharmacy or health store around you."}
    return messages.get(key_value, SOMETHING_IS_WRONG)


class ValidateRequest03MonthsForm(FormValidationAction):

    def name(self):
        return 'validate_request_0_3_months_form'

    def validate_daily_medical_conditions(self,
                                          slot_value: Any,
                                          dispatcher: CollectingDispatcher,
                                          tracker: Tracker,
                                          domain: DomainDict,
                                          ):
        print("in validate medical condition")
        print(slot_value)
        if slot_value.lower() == 'yes':
            dispatcher.utter_message(text="Ok, it is not advisable for you to take daily pills. "
                                          "Please speak to your doctor before using this method of contraceptive.")

        return {'daily_medical_conditions': slot_value}

    def validate_daily_contraceptive_database(self,
                                              slot_value: Any,
                                              dispatcher: CollectingDispatcher,
                                              tracker: Tracker,
                                              domain: DomainDict,
                                              ):

        print(f"in solt validate daily contraceptive database: {slot_value}")
        dispatcher.utter_message(text=get_daily_contraceptive_database_message(slot_value))
        return {'daily_contraceptive_database': slot_value}

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[Text]:
        slots = domain_slots.copy()

        if get_slot_value(tracker, '0_3_months_method') == "Daily contraceptive pills":
            print("inside if else")
            slots = remove_slot_values(slots, "daily")
        elif get_slot_value(tracker, '0_3_months_method') == "Emergency contraceptive pills":
            slots = remove_slot_values(slots, "emergency")
        print(f"Slot info after removing: {slots}")

        if get_slot_value(tracker, 'daily_medical_conditions') == "Yes":
            slots.remove('daily_contraceptive_database')

        return slots
