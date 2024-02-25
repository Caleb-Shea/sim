import pygame as pyg
import os

from color import Color
from world import World


class Game():
    def __init__(self) -> None:

        # Bookkeeping variables
        self.window = pyg.display.get_surface()
        self.WIN_W, self.WIN_H = pyg.display.get_window_size()
        self.clock = pyg.time.Clock()
        self.FPS = 30
        self.paused = False

        # Game vars
        self.world = World()
        self.entities = []

        self.world.initial_generate(force_new=False)

        self.font = pyg.font.SysFont(None, 24)
    
    @staticmethod
    def _quit_game() -> None:
        """Cleanly exit the program."""
        pyg.quit()
        raise SystemExit(0)

    @staticmethod
    def _play_sound(sound: pyg.mixer.Sound) -> None:
        """Begin playing a sound on any available sound channel."""
        se_channel = pyg.mixer.find_channel()
        se_channel.play(sound)
    
    @staticmethod    
    def _get_path(path: str) -> str:
        """Returns the full file path of a file as a string."""
        dirname = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(dirname, path)

    def save_to_file(self) -> None:
        """Save the current game state to a file."""
        ...
    
    def load_from_file(self) -> None:
        """Load a game state from a file."""
        ...
        
    def handle_inputs(self):
        """Handle all user inputs"""

        # Events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                Game._quit_game()
            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    self.paused = True
                elif event.key == pyg.K_BACKQUOTE:
                    Game._quit_game()
                elif event.key == pyg.K_SPACE:
                    self.world.set_zoom()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                ...
            elif event.type == pyg.MOUSEWHEEL:
                self.world.zoom(2*event.y, pyg.mouse.get_pos())
        
        # Keyboard input
        keys = pyg.key.get_pressed()
        if keys[pyg.K_SPACE]:
            ...
        if keys[pyg.K_a]:
            self.world.zoom(2, (self.WIN_W/2, self.WIN_H/2))

        if keys[pyg.K_z]:
            self.world.zoom(-2, (self.WIN_W/2, self.WIN_H/2))


        # Mouse input
        m_but = pyg.mouse.get_pressed()
        m_rel = pyg.mouse.get_rel()
        if m_but[0]:
            self.world.pan(m_rel)

    def update(self):
        ...

    def render_world(self):
        self.world.render()

    def render_entities(self):
        ...

    def render_UI(self):
        a = self.font.render(f"Cells Rendered: {self.world.num_cells_rendered}", True, (0, 0, 0), (255, 255, 255))
        self.window.blit(a, (10, 10))

        a = self.font.render(f"X offset: {self.world.off_x}", True, (0, 0, 0), (255, 255, 255))
        self.window.blit(a, (10, 30))

        a = self.font.render(f"Y offset: {self.world.off_y}", True, (0, 0, 0), (255, 255, 255))
        self.window.blit(a, (10, 50))

        a = self.font.render(f"m_pos: {pyg.mouse.get_pos()}", True, (0, 0, 0), (255, 255, 255))
        self.window.blit(a, (10, 70))

    def render(self):
        """Update the window with the current state of the game."""

        self.window.fill(Color.BG)

        self.render_world()
        self.render_entities()
        self.render_UI()

        # Push this frame
        pyg.display.flip()

        # Manage framerate
        self.clock.tick(self.FPS)