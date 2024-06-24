import keyboard


def on_key_press(event, character):
    character.cache_direction = event.name[0]
