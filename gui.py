import argparse
import sys

from blessed import Terminal

import arena

def render_stats():
    print(f'Tick {arena.i:3}, Kills {arena.player.kills:3}')

t = Terminal()
with t.fullscreen():
    inp = None
    with t.location(0, 0):
        render_stats()
        arena.render_world()
    while inp != 'q':
        with t.cbreak():
            inp = t.inkey()
            if inp == 'k' or inp == t.KEY_UP:
                arena.player.up()
            elif inp == 'j' or inp == t.KEY_DOWN:
                arena.player.down()
            elif inp == 'h' or inp == t.KEY_LEFT:
                arena.player.left()
            elif inp == 'l' or inp == t.KEY_RIGHT:
                arena.player.right()
            elif inp == ' ':
                arena.player.attack_nearest()
            arena.tick()
            with t.location(0, 0):
                render_stats()
                arena.render_world()
