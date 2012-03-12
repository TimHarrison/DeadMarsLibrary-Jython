'''
Created on Mar 11, 2012

@author: tharrison
'''

from src.system.time_span import TimeSpan

class GameTime:
    elapsed_game_time = TimeSpan()
    elapsed_real_time = TimeSpan()
    total_game_time = TimeSpan()
    total_real_time = TimeSpan()