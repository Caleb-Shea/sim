class Color():
    """Store all the colors used in the game."""
    BLUE = (0, 0, 200)
    BG = (200, 230, 200)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Colors with alpha values
    CLEAR = (0, 0, 0, 0)

    @staticmethod
    def darken(color: tuple, amt: float) -> tuple:
        """Darken a color by a given percentage amount.""" 

        # Decrease each RGB value by the provided amount
        if len(color) == 3:
            return (color[0] * (1-amt),
                    color[1] * (1-amt),
                    color[2] * (1-amt))
        
        # Keep alpha values the same but darken the rest
        elif len(color) == 4:
            return (color[0] * (1-amt),
                    color[1] * (1-amt),
                    color[2] * (1-amt),
                    color[3])
        
        raise ValueError("Incorrect parameters")

    @staticmethod
    def lighten(color: tuple, amt: int) -> tuple:
        """Lighten a color by a given amount."""

        # Increase each RGB value by the provided amount
        if len(color) == 3:
            return (color[0] * (1-amt),
                    color[1] * (1-amt),
                    color[2] * (1-amt))
        
        # Keep alpha values the same but lighten the rest
        elif len(color) == 4:
            return (color[0] * (1+amt),
                    color[1] * (1+amt),
                    color[2] * (1+amt),
                    color[3])
        
        raise ValueError("Incorrect parameters")