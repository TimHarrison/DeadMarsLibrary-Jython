'''
Created on Mar 11, 2012

@author: tharrison
'''
from src.game.game_input import GameInput
from src.screen_manager import ScreenState
from src.system.time_span import TimeSpan

class Screen():
    _is_popup = False
    _screen_state = ScreenState.transition_on
    _transition_time_on = TimeSpan.zero()
    _transition_time_off = TimeSpan.zero()
    _transition_position = 1
    _is_exiting = False
    _other_screen_has_focus = False
    