obs = obslua

function find_source_by_name_in_list(source_list, name)
  for i, source in pairs(source_list) do
    source_name = obs.obs_source_get_name(source)
    if source_name == name then
      return source
    end
  end

  return nil
end

function set_scene_by_name(scene_name)
  local scenes = obs.obs_frontend_get_scenes()

  local scene = find_source_by_name_in_list(scenes, scene_name)
  obs.obs_frontend_set_current_scene(scene)

  obs.source_list_release(scenes)
end

function script_load(settings)
end

function script_unload()
end
