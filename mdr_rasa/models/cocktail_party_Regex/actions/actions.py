from typing import Any, Dict, List, Text
from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, Action

class RequestOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_request_order_form"

    def __init__(self) -> None:
        self.valid_locations = self._read_valid_values("valid_locations.txt")
        self.valid_objects = self._read_valid_values("valid_objects.txt")

    def _read_valid_values(self, file_path: str) -> List[str]:
        values = []
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    values.append(line.strip())
        except Exception as e:
            print(f"Error reading values from file: {str(e)}")
        return values

    def validate_location(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if value.lower() not in self.valid_locations:
            dispatcher.utter_message("Sorry, I don't recognize that location.")
            return {"location": None}
        return {"location": value}

    def validate_object(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if value.lower() not in self.valid_objects:
            dispatcher.utter_message("Sorry, I don't recognize that object.")
            return {"object": None}
        return {"object": value}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Great! I will bring the requested item from the specified location.")
        return []

class ActionAskFormSlots(Action):
    def name(self) -> Text:
        return "action_ask_form_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.active_form.get("name") == "request_order_form" and not all(tracker.get_slot(slot) for slot in ["location", "object"]):
            for slot in ["location", "object"]:
                if tracker.get_slot(slot) is None:
                    dispatcher.utter_message(template=f"utter_ask_{slot}")
                    return [SlotSet("requested_slot", slot)]
        return []

