import obspython as obs
import urllib.request
import json

IN_GAME = 'sc2_switcher_in_game'
OUT_OF_GAME = 'sc2_switcher_out_of_game'


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
    with urllib.request.urlopen("http://localhost:6119/ui") as response:
        ui_data = json.load(response)
    num_active_screens = len(ui_data.get('activeScreens', []))
    with urllib.request.urlopen("http://localhost:6119/game") as response:
        game_data = json.load(response)
    display_time = game_data.get("displayTime", 0.0)

    return num_active_screens == 0 and display_time > 0.0


def switch_scene():
    try:
        scene_name = IN_GAME if is_in_game() else OUT_OF_GAME
        set_scene_by_name(scene_name)
    except:
        pass


def script_load(settings):
    obs.timer_add(switch_scene, 500)


def script_unload():
    obs.timer_remove(switch_scene)
