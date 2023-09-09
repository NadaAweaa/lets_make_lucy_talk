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
