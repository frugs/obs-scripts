OBS Studio SCII Scene Switcher
==============================

Installation Instructions
-------------------------

### Windows

- Extract _OBS Studio SCII Scene Switcher_ into a directory of your
  choosing.
- Inside OBS Studio, navigate to 'Tools' -> 'Scripts'.
- Switch to the 'Python Settings' tab, then set the 'Python Install
  Path' to the `python36` directory inside the directory you extracted
  _OBS Studio SCII Scene Switcher_ to.
- Switch back to the 'Scripts' tab, then click the '+' button to add a
  new script.
- Navigate to the directory you extracted _OBS Studio SCII Scene
  Switcher_ to, then select the file `sc2_scene_switcher.py`
- The script should now be enabled and ready to use!

Usage Instructions
------------------

- Inside OBS Studio, create two scenes: one named `sc2_switcher_in_game`
  and the other named `sc2_switcher_out_of_game`. You can alternatively
  just rename two existing scenes to these names as well.
- While the script is enabled, the former scene will be set as the
  active scene when StarCraft II enters a game, and the latter scene
  will be set as the active scene when StarCraft II exits a game.
- Feel free to manually switch between scenes while the script is
  active, but be aware that the script will still try and switch to the
  appropriate scene when it detects that a StarCraft II game has started
  or finished.