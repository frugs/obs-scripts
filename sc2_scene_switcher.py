import obspython as obs
import urllib.request
import json
import threading
import asyncio

IN_GAME = 'sc2_switcher_in_game'
OUT_OF_GAME = 'sc2_switcher_out_of_game'

event_loop = asyncio.new_event_loop()
event_loop_thread = None
prev_in_game = None


def find_source_by_name_in_list(source_list, name):
    for source in source_list:
        source_name = obs.obs_source_get_name(source)
        if source_name == name:
            return source
    return None


def set_scene_by_name(scene_name):
    scenes = obs.obs_frontend_get_scenes()

    scene = find_source_by_name_in_list(scenes, scene_name)
    if scene is not None:
        obs.obs_frontend_set_current_scene(scene)

    obs.source_list_release(scenes)


def is_in_game():
    try:
        with urllib.request.urlopen("http://localhost:6119/ui") as response:
            ui_data = json.load(response)
        num_active_screens = len(ui_data.get('activeScreens', []))
        with urllib.request.urlopen("http://localhost:6119/game") as response:
            game_data = json.load(response)
        display_time = game_data.get("displayTime", 0.0)

        return num_active_screens == 0 and display_time > 0.0
    except Exception:
        return None


def run_event_loop():
    global event_loop
    event_loop.run_forever()


def stop_event_loop():
    global event_loop
    event_loop.stop()


def switch_scene():
    global prev_in_game

    cur_in_game = is_in_game()
    if cur_in_game is not None and (prev_in_game is None
                                    or cur_in_game != prev_in_game):
        prev_in_game = cur_in_game
        scene_name = IN_GAME if cur_in_game else OUT_OF_GAME
        set_scene_by_name(scene_name)


def queue_switch_scene():
    global event_loop
    event_loop.call_soon_threadsafe(switch_scene)


def script_load(settings):
    global event_loop_thread

    event_loop_thread = threading.Thread(target=run_event_loop)
    event_loop_thread.start()
    obs.timer_add(queue_switch_scene, 1500)


def script_unload():
    global event_loop_thread

    obs.timer_remove(queue_switch_scene)
    event_loop.call_soon_threadsafe(stop_event_loop)
    event_loop_thread.join()
