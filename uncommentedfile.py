#!/usr/bin/python
# -*- coding: utf-8 -*-

class UnCommentedFile:
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring
    def next(self):
        line = self.f.next()
#         while line.startswith(self.commentstring):
#             pass
#             line = line[1:]
        return line
    def __iter__(self):
        return self
        