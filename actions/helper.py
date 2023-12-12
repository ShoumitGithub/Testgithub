from typing import List

from rasa_sdk import Tracker


def create_button(button_message_details: List):

    button_details = []
    for message in button_message_details:
        button_details.append({"title": message, "payload": message})
    return button_details


def create_hyper_link(url: str, url_description: str):

    return f'<a href="{url}">{url_description}</a>'


def remove_slot_values(slots: List, search_text: str):
    for slot in slots:
        if not slot.startswith(search_text):
            slots.remove(slot)
    print(f"inside remove slots {slots}")
    return slots

