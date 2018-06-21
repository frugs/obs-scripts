import obspython as obs
import urllib.request
import json
import threading
import asyncio

IN_GAME = 'sc2_switcher_in_game'
OUT_OF_GAME = 'sc2_switcher_out_of_game'

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
    asyncio.get_event_loop().run_forever()


async def stop_event_loop():
    asyncio.get_event_loop().stop()


async def switch_scene():
    cur_in_game = await asyncio.get_event_loop().run_in_executor(
        None, is_in_game())
    if cur_in_game is not None and (prev_in_game is None
                                    or cur_in_game != prev_in_game):
        scene_name = IN_GAME if cur_in_game else OUT_OF_GAME
        await asyncio.get_event_loop().run_in_executor(
            None, set_scene_by_name(scene_name))


def queue_switch_scene():
    asyncio.get_event_loop().call_soon_threadsafe(switch_scene())


def script_load(settings):
    event_loop_thread = threading.Thread(target=run_event_loop)
    event_loop_thread.start()
    obs.timer_add(queue_switch_scene, 500)


def script_unload():
    obs.timer_remove(queue_switch_scene)
    future = asyncio.run_coroutine_threadsafe(stop_event_loop(),
                                              asyncio.get_event_loop())
    future.result(2)
    event_loop_thread.join(2)
