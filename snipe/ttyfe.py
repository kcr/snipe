# -*- encoding: utf-8 -*-


import os
import curses
import locale
import signal
import logging
import itertools

from . import mux


class TTYRenderer(object):
    def __init__(self, ui, y, x, h, w, window):
        self.ui, self.y, self.x, self.width, self.height = ui, y, x, w, h
        self.window = window
        self.window.renderer = self
        self.w = ui.stdscr.subwin(h, w, y, x)
        self.w.idlok(1)
        #self.w.scrollok(1)
        self.log = logging.getLogger('TTYRender.%x' % (id(self),))
        self.frame = None
        self.context = None

    @property
    def active(self):
        return self.ui.active == self

    def write(self, s):
        self.log.debug('someone used write(%s)', repr(s))

    def redisplay(self):
        if self.frame is None:
            self.log.debug('redisplay with no frame, firing reframe')
            self.reframe()
        visible = self.redisplay_internal()
        if not visible:
            self.log.debug('redisplay, no visibility, firing reframe')
            self.reframe()
            visible = self.redisplay_internal()
            if not visible:
                self.log.debug('redisplay, no visibility after reframe')
        self.w.noutrefresh()

    @staticmethod
    def doline(s, width, remaining):
        '''string, window width, remaining width ->
        iter([(displayline, remaining), ...])'''
        # turns tabs into spaces at n*8 cell intervals
        #XXX needs initial offset for tab stops
        #and for width after newline
        out = ''
        col = 0 if remaining is None or remaining <= 0 else width - remaining
        for c in s:
            # XXX Unicode width, combining characters, etc.
            if c == '\n':
                yield out, -1
                out = ''
                col = 0
            elif ' ' <= c <= '~': #XXX should look up unicode category
                if col >= width:
                    yield out, 0
                    out = ''
                    col = 0
                out += c
                col += 1
            elif c == '\t':
                n = (8 - col % 8)
                if col + n >= width:
                    yield out, 0
                    out = ''
                    col = 0
                else:
                    col += n
                    out += ' ' * n
            # non printing characters... don't
        if out:
            yield out, width - col

    def redisplay_internal(self):
        self.log.debug(
            'in redisplay_internal: w=%d, h=%d, frame=%s',
            self.width,
            self.height,
            repr(self.frame),
            )

        self.w.erase()
        self.w.move(0,0)

        visible = False
        cursor = None
        screenlines = self.height
        remaining = None

        for mark, chunk in self.window.view(self.frame):
            for tags, text in chunk:
                if screenlines <= 0:
                    break
                if 'cursor' in tags:
                    cursor = self.w.getyx()
                if 'visible' in tags:
                    visible = True
                for line, remaining in self.doline(text, self.width, remaining):
                    self.w.addstr(line)
                    if remaining <= 0:
                        screenlines -= 1
                    if screenlines <= 0:
                        break
                    if remaining == -1:
                        self.w.addstr('\n')
                    elif remaining == 0:
                        self.w.move(self.height - screenlines, 0)
        if cursor is not None and self.active:
            self.w.leaveok(0)
            self.w.move(*cursor)
        else:
            self.w.leaveok(1)
        self.log.debug(
            'redisplay internal exiting, cursor=%s, visible=%s',
            repr(cursor),
            repr(visible),
            )
        return visible

    def reframe(self):
        screenlines = self.height / 2
        ## view = iter(self.window.view(self.cursor, 'backward'))
        ## mark, chunk = view.next()
        ## self.frame = mark
        ## chunk = itertools.takewhile(
        ##     lambda: 'visible' not in x[0],
        ##     chunk)
        ## chunklines = list(self.doline(''.join(c[1] for c in chunk)))
        ## # if len(chunklines) - 1 > self.height: *sob*
        self.log.debug('reframe, previous frame=%s', repr(self.frame))
        for mark, chunk in self.window.view(self.window.cursor, 'backward'):
            self.frame = mark
            # this should only drop stuff off the first chunk...
            chunk = itertools.takewhile(
                lambda x: 'visible' not in x[0],
                chunk)
            chunklines = list(self.doline(''.join(c[1] for c in chunk), self.width, self.width))
            screenlines -= len(chunklines)
            if screenlines <= 0:
                break

unkey = dict(
    (getattr(curses, k), k[len('KEY_'):])
    for k in dir(curses)
    if k.startswith('KEY_'))
key = dict(
    (k[len('KEY_'):], getattr(curses, k))
    for k in dir(curses)
    if k.startswith('KEY_'))


class TTYFrontend(mux.Muxable):
    reader = True
    handle = 0 # stdin

    def __init__(self):
        self.stdscr, self.maxy, self.maxx, self.active = (None,)*4
        self.windows = []
        self.notify_silent = True

    def __enter__(self):
        locale.setlocale(locale.LC_ALL, '')
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.raw()
        self.stdscr.keypad(1)
        curses.start_color()
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.orig_sigtstp = signal.signal(signal.SIGTSTP, self.sigtstp)
        return self

    def initial(self, win):
        if self.windows or self.active:
            raise ValueError
        self.active = TTYRenderer(self, 0, 0, self.maxy, self.maxx, win)
        self.windows = [self.active]
        self.active.w.refresh()
        self.stdscr.refresh()

    def __exit__(self, type, value, tb):
        # go to last line of screen, maybe cause scrolling?
        self.stdscr.keypad(0)
        curses.noraw()
        curses.echo()
        curses.endwin()
        signal.signal(signal.SIGTSTP, self.orig_sigtstp)

    def sigtstp(self, signum, frame):
        curses.def_prog_mode()
        curses.endwin()
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)
        os.kill(os.getpid(), signal.SIGTSTP)
        signal.signal(signal.SIGTSTP, self.sigtstp)
        self.stdscr.refresh()

    def write(self, s):
        pass #XXX put a warning here or a debug log or something

    def doresize(self):
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        # rearrange windows as appropriate and trigger redisplays

    def getch(self):
        c = self.stdscr.getch()
        #XXX do something clever with UTF-8 (IFF we are in a UTF-8 locale)
        if c == curses.KEY_RESIZE:
            self.doresize()
            ## self.write('(%d, %d)\n' % (self.maxy, self.maxx))
        if -1 < c < 256:
            return chr(c)
        if c in unkey:
            return unkey[c]
        return c

    def readable(self):
        k = self.getch()
        if self.active:
            self.active.window.input_char(k)
        self.redisplay()

    def redisplay(self):
        for w in self.windows:
            if w is not self.active:
                w.redisplay()
        self.active.redisplay()
        curses.doupdate()

    def notify(self):
        if self.notify_silent:
            curses.flash()
        else:
            curses.beep()
