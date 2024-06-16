from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionSetReminder(Action):

    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract entities from the user message
        reminder_time = next(tracker.get_latest_entity_values("time"), None)
        reminder_task = next(tracker.get_latest_entity_values("task"), None)

        if reminder_time and reminder_task:
            # Set the reminder (this is where you would integrate with a reminder service)
            dispatcher.utter_message(text=f"Reminder set for {reminder_task} at {reminder_time}")
        else:
            dispatcher.utter_message(text="I couldn't understand the reminder details.")

        return []
    
class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')
        if not location:
            dispatcher.utter_message(text="Please provide a location to get the weather update.")
            return []

        # Example of a weather API call
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={location}")
        weather_data = response.json()

        if response.status_code == 200 and 'current' in weather_data:
            temp_c = weather_data['current']['temp_c']
            condition = weather_data['current']['condition']['text']
            dispatcher.utter_message(text=f"The current temperature in {location} is {temp_c}°C with {condition}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the weather for that location.")
        
        return []
