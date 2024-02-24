from entities import Entity

class StatTracker():
    def __init__(self) -> None:
        pass


class EntityStatTracker(StatTracker):
    """
    Track the statistics of an object cause data is cool.
    
    Stuff like time alive, steps moved, actions taken etc.

    *Not attributes like movement speed or aggressions.
    """
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

        self.time_alive = 0
        self.birth_date = ""
        self.death_date = ""
        self.action_list = []
        self.distance_moved = 0
        self.entities_killed = []
        self.damage_taken = 0
        self.damage_dealt = 0
        self.generation = 0
        self.rivers_crossed = 0
        self.time_asleep = 0
        self.num_sleeps = 0
        self.things_eaten = []
        self.time_in_water = 0
        self.time_in_forest = 0
        self.time_in_plains = 0


class GameStatTracker(StatTracker):
    ...