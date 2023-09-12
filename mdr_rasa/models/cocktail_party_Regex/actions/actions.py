# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ValidateSimpleOrderForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_simple_order_form"

    def __init__(self) -> None:
        self.valid_locations = ["living_room", "kitchen_counter", "dining_table","hall", "shelf"]
        self.valid_objects = ["pringles","windex_bottle","soup","shirt","spatula"]

    def validate_places(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if value.lower() not in self.valid_locations:
            # dispatcher.utter_message("Sorry, I don't recognize that location.")
            dispatcher.utter_template("utter_ask_places_again", tracker)
            return {"places": None}
        return {"places": value}

    def validate_order(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if value.lower() not in self.valid_objects:
            # dispatcher.utter_message("Sorry, I don't recognize that object.")
            dispatcher.utter_template("utter_ask_order_again", tracker)
            return {"order": None}
        return {"order": value}

class ActionCustomFallback(Action):
    def name(self) -> Text:
        return "action_fallback_response"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Send a message to the user
        dispatcher.utter_response("utter_fallback")

        # Return an empty list
        return []

class ActionClearSlot(Action):
    def name(self) -> Text:
        return "action_clear_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # add all the slots you wish to clear, here:
        # TODO: can also use return [AllSlotsReset()] if always clearing all slots. 
        return [SlotSet("order", None), SlotSet("places",None), SlotSet("confirmation", None)]
