'''
Created on Mar 11, 2012

@author: tharrison
'''
class TimeSpan:
    def __init__(self):
        self.span = 0
        self.start = 0
        self.end = 0


    def set_span(self, time_span):
        self.span = time_span
        self.start = 0
        self.end = time_span


    def get_seconds(self):
        return self.span