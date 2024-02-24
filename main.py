import pygame as pyg

from game import Game

"""
TODO: Clamp map panning so you don't see background
TODO: Optimize the rendering of the cells
TODO: Loading screen when creating new heightmaps
TODO: Optimize World.render() on-screen check
TODO: Mouse scroll sensitivity setting somewhere (Game.handle_inputs())
"""

def main():

    # --- Pygame init ---
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("Sim")
    pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)

    # --- Program setup ---
    game = Game()

    # --- Game loop ---
    while True:
        if not game.paused:
            game.handle_inputs()
            game.update()
            game.render()

        else: # If paused
            ...

if __name__ == '__main__':
    # Start the game
    main()
