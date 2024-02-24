from stat_trackers import EntityStatTracker

class Entity():
    """
    An entity in the game world.
    This class stores information about the entity and allows for rendering
    with its world-form or its card-form.
    """
    def __init__(self) -> None:
        self.stats = EntityStatTracker(self)

    def analyze_world(self):
        """Look at the world and decide priorities."""
        pass
    
    def move(self):
        """Update this entity's position in the world."""
        pass
    
    def render(self):
        """Draw this entity to the window."""
        pass

class Dog(Entity):
    def __init__(self) -> None:
        super().__init__()


class Squirrel(Entity):
    def __init__(self) -> None:
        super().__init__()


class Tree(Entity):
    def __init__(self) -> None:
        super().__init__()


class Rock(Entity):
    def __init__(self) -> None:
        super().__init__()