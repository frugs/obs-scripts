import obspython as obs


def find_source_by_name_in_list(source_list, name):
    for source in source_list:
        source_name = obs.obs_source_get_name(source)
        if source_name == name:
            return source
    return None


def set_scene_by_name(scene_name):
    scenes = obs.obs_frontend_get_scenes()

    scene = find_source_by_name_in_list(scenes, scene_name)
    obs.obs_frontend_set_current_scene(scene)

    obs.source_list_release(scenes)


def script_load(settings):
    set_scene_by_name("blah2")
    pass


def script_unload():
    pass
