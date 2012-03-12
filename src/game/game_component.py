'''
Created on Mar 11, 2012

@author: tharrison
'''
import java.awt.Graphics as Graphics
import javax.swing.JComponent as JComponent

class GameComponent(JComponent):
    
    def __init__(self, game):
        self.game = game
    
    def initialize(self):
        return self
    
    def load_content(self):
        return self
    
    def unload_content(self):
        return self
    
    def update(self, game_time):
        return self
    
    def render(self, game_time, Graphics):
        return self