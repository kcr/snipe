# -*- encoding: utf-8 -*-
# Copyright © 2014 Karl Ramm
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


"""
Unit tests for the TTY frontend objects

(hard because we haven't mocked curses yet.)
"""

import sys
import unittest

sys.path.append('..')
import snipe.ttyfe


class TestTTYFE(unittest.TestCase):
    def testTTYRendererDoline(self):
        self.assertEqual(
            list(snipe.ttyfe.TTYRenderer.doline('abc', 80, 80)),
            [('abc', 77)])
        self.assertEqual(
            list(snipe.ttyfe.TTYRenderer.doline("\tabc", 80, 0)),
            [('        abc', 69)])
        self.assertEqual(
            list(snipe.ttyfe.TTYRenderer.doline('abc\n', 80, 80)),
            [('abc', -1)])
        self.assertEqual(
            list(snipe.ttyfe.TTYRenderer.doline('a\01bc', 80, 80)),
            [('abc', 77)])
        self.assertEqual(
            list(snipe.ttyfe.TTYRenderer.doline('abcdef', 3, 3)),
            [('abc', 0), ('def', 0)])
        self.assertEqual(
            list(snipe.ttyfe.TTYRenderer.doline('ab\tdef', 3, 3)),
            [('ab', 0), ('def', 0)])

    def testMockWindow(self):
        w = MockWindow([''])
        self.assertEqual(list(w.view(0, 'forward')), [(0, [((), '')])])
        w = MockWindow(['abc\n', 'def\n'])
        self.assertEqual(
            list(w.view(0, 'forward')),
            [
                (0, [((), 'abc\n')]),
                (1, [((), 'def\n')]),
            ])

    def testLocation0(self):
        w = MockWindow([''])
        self.assertEqual(list(w.view(0, 'forward')), [(0, [((), '')])])
        ui = MockUI()
        renderer = snipe.ttyfe.TTYRenderer(ui, 0, 24, w)
        l = snipe.ttyfe.Location(renderer, 0, 0)
        m = l.shift(100)
        self.assertEqual(l.cursor, m.cursor)
        self.assertEqual(l.offset, m.offset)
        m = l.shift(-100)
        self.assertEqual(l.cursor, m.cursor)
        self.assertEqual(l.offset, m.offset)

    def testLocation1(self):
        w = MockWindow(['abc\n', 'def'])
        ui = MockUI()
        renderer = snipe.ttyfe.TTYRenderer(ui, 0, 24, w)

        l = snipe.ttyfe.Location(renderer, 0, 0)
        self.assertEqual(l.cursor, 0)
        self.assertEqual(l.offset, 0)
        m = l.shift(100)
        self.assertEqual(m.cursor, 1)
        self.assertEqual(l.offset, 0)

        m = l.shift(1)
        self.assertEqual(m.cursor, 1)
        self.assertEqual(l.offset, 0)

        m = m.shift(-1)
        self.assertEqual(l.cursor, m.cursor)
        self.assertEqual(l.offset, m.offset)

    def testLocation2(self):
        w = MockWindow(['abc\n', 'def\n', 'ghi\n', 'jkl'])
        ui = MockUI()
        renderer = snipe.ttyfe.TTYRenderer(ui, 0, 24, w)

        l = snipe.ttyfe.Location(renderer, 0, 0)
        self.assertEqual(l.cursor, 0)
        self.assertEqual(l.offset, 0)
        m = l.shift(100)
        self.assertEqual(m.cursor, 3)
        self.assertEqual(l.offset, 0)

        m = l.shift(3)
        self.assertEqual(m.cursor, 3)
        self.assertEqual(l.offset, 0)

        m = m.shift(-3)
        self.assertEqual(l.cursor, m.cursor)
        self.assertEqual(l.offset, m.offset)

    def testLocation2(self):
        w = MockWindow(['abc\nabc\n', 'def\n', 'ghi\n', 'jkl'])
        ui = MockUI()
        renderer = snipe.ttyfe.TTYRenderer(ui, 0, 24, w)

        l = snipe.ttyfe.Location(renderer, 0, 0)
        self.assertEqual(l.cursor, 0)
        self.assertEqual(l.offset, 0)
        m = l.shift(100)
        self.assertEqual(m.cursor, 3)
        self.assertEqual(l.offset, 0)

        m = l.shift(3)
        self.assertEqual(m.cursor, 2)
        self.assertEqual(l.offset, 0)

        m = m.shift(-3)
        self.assertEqual(l.cursor, m.cursor)
        self.assertEqual(l.offset, m.offset)


class MockCursesWindow:
    def subwin(self, *args):
        return self
    def idlok(slef, *args):
        pass


class MockUI:
    def __init__(self, maxx=80):
        self.stdscr = MockCursesWindow()
        self.maxx = maxx


class MockWindow:
    hints = {}
    def __init__(self, chunks):
        self.chunks = [[((), chunk)] for chunk in chunks]
    def view(self, origin, direction='forward'):
        assert direction in ('forward', 'backward')
        if direction == 'forward':
            r = range(origin, len(self.chunks))
        elif direction == 'backward':
            r = range(origin, -1, -1)
        for i in r:
            yield i, self.chunks[i]


if __name__ == '__main__':
    unittest.main()
