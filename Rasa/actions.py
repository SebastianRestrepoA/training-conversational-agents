# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
# rasa run actions --port 9000 --debug

from typing import Any, Text, Dict, List, Union
import requests

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import json


class ActionSaludo(Action):

    def name(self) -> Text:
        return "action_saludo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="¡Hola! ¿En que te puedo colaborar?")

        return []


class ActionDespedida(Action):

    def name(self) -> Text:
        return "action_despedida"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Ok! seguire disponible por si me necesitas!")

        return []


