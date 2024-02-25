import pygame as pyg
from perlin_noise import PerlinNoise

from color import Color


class World():
    """
    The world entities live in.
    
    Psuedo-randomly generated

    *Does not track entity information.
    """

    def __init__(self) -> None:
        self.window = pyg.display.get_surface()
        self.WIN_W, self.WIN_H = pyg.display.get_window_size()

        self.cell_size = 10
        self.default_cell_size = self.cell_size

        self.pan_border = 2 * self.default_cell_size

        self.off_x = 0
        self.off_y = 0

        self.areas = []
        self.chunks = []

        self.noise = PerlinNoise(octaves=10)
        self.heightmap = []

        self.num_cells_rendered = 0
    
    def _FBM(self, x: float, y: float) -> float:
        """
        Fractional Brownian Motion function taken from
        https://rtouti.github.io/graphics/perlin-noise-algorithm.
        """
        result = 0
        amp = 1 # Doesn't matter cause we normalize it later
        freq = .1 # Make bigger to stretch (smooth) the field

        for _ in range(8):
            result += amp * self.noise([x*freq, y*freq])

            amp *= 0.5
            freq *= 2
        
        return result

    def initial_generate(self, force_new=False) -> None:
        """Use Perlin noise and FBM to generate an inital landscape."""

        raw_noise = []

        # Check if there is anything saved to load instead
        try:
            # Raise an exception if we want new data
            if force_new:
                raise Exception
            
            # Open the noise file and save it into memory
            with open("save/raw_noise.txt", "r") as f:

                # Read first line for validation
                header = f.readline()
                if header != f"{self.default_cell_size}\n":
                    raise Exception

                # Read the rest of the file
                for line in f.readlines():

                    # Make sure to convert everything to numbers
                    raw_noise.append(list(map(float, line.split())))

        # If nothing exists we need to create the noise anew
        except Exception as e:
        
            # Generate a noise base
            for y in range(self.WIN_H//self.cell_size):
                row = []
                for x in range(self.WIN_W//self.cell_size):
                    row.append(self._FBM(x/(self.WIN_W//self.cell_size),
                                         y/(self.WIN_H//self.cell_size)))
                raw_noise.append(row)
            
            # Save the noise so we don't have to recreate it next time
            with open("save/raw_noise.txt", "w") as f:

                # Write header
                f.write(f"{self.default_cell_size}\n")

                # Write file contents
                for row in raw_noise:
                    f.write(" ".join(map(str, row)) + "\n")
        
        max_ = max([max(row) for row in raw_noise])
        min_ = min([min(row) for row in raw_noise])

        # Normalize the noise to 0-1
        for row in raw_noise:
            tmp = []

            for val in row:
                tmp.append((val-min_) / (max_-min_))
            
            self.heightmap.append(tmp)

        # Save original heightmap
        self.base_heightmap = self.heightmap[:]
    
    def set_zoom(self, lvl=0) -> None:
        """Set the zoom level. If no lvl paramter is passed, will default
        to filling the screen exactly."""

        if lvl < self.default_cell_size:
            self.cell_size = self.default_cell_size
            self.off_x = 0
            self.off_y = 0
        else:
            amt = lvl - self.cell_size

            self.cell_size = lvl

            # Update cam values so we zoom based on the middle of the screen
            self.off_x += ((self.off_x - self.WIN_W/2)*amt/(self.cell_size-amt))
            self.off_y += ((self.off_y - self.WIN_H/2)*amt/(self.cell_size-amt))
    
    def zoom(self, amt: int, tgt: tuple) -> None:
        """Zoom in/out, centered on tgt, by the specified amount.
        Positive numbers zoom in and negative numbers zoom out"""

        # Update the cell size
        self.cell_size += amt

        # Clamp cell size to the default size to prevent /0 errors
        if self.cell_size < self.default_cell_size:
            self.cell_size = self.default_cell_size
            return

        # Diff from target to tl corner
        diff_x = self.off_x - tgt[0]
        diff_y = self.off_y - tgt[1]

        # Scale diff based on amt
        diff_x = (diff_x*amt/(self.cell_size-amt))
        diff_y = (diff_y*amt/(self.cell_size-amt))

        # Offset camera
        self.off_x += diff_x
        self.off_y += diff_y

        # Clamp
        mw = self.cell_size * len(self.heightmap[0])
        mh = self.cell_size * len(self.heightmap)

        self.off_x = min(self.pan_border, self.off_x)
        self.off_x = max(self.WIN_W - mw - self.pan_border, self.off_x)

        self.off_y = min(self.pan_border, self.off_y)
        self.off_y = max(self.WIN_H - mh - self.pan_border, self.off_y)
    
    def pan(self, amt: tuple) -> None:
        """Pan the camera by a given amount."""

        # Move camera
        self.off_x += amt[0]
        self.off_y += amt[1]

        # Clamp
        mw = self.cell_size * len(self.heightmap[0])
        mh = self.cell_size * len(self.heightmap)

        self.off_x = min(self.pan_border, self.off_x)
        self.off_x = max(self.WIN_W - mw - self.pan_border, self.off_x)

        self.off_y = min(self.pan_border, self.off_y)
        self.off_y = max(self.WIN_H - mh - self.pan_border, self.off_y)

    def render(self):
        self.num_cells_rendered = 0

        for j, row in enumerate(self.heightmap):
            for i, val in enumerate(row):
                
                # Check if the cell we're about to render is actually on-screen
                if not (-self.cell_size < i*self.cell_size + self.off_x < self.WIN_W) \
                    or not (-self.cell_size < j*self.cell_size + self.off_y < self.WIN_H):
                        continue

                r = (i*self.cell_size + self.off_x,
                     j*self.cell_size + self.off_y,
                     self.cell_size,
                     self.cell_size)
                pyg.draw.rect(self.window, (val*255, 0, val*255), r)

                self.num_cells_rendered += 1