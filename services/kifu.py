from copy import deepcopy

class Tank():
    DIRECTION_REF = {'n': 'north', 'ne': 'north_east', 'e': 'east',
                     'se': 'south_east', 's': 'south', 'sw': 'south_west',
                     'w': 'west', 'nw': 'north_west'}

    def __init__(self, color, tank_type, direction):
        self.color = color
        self.tank_type = tank_type
        self.direction = direction
        self.destroyed = False
    
    def map_display(self):
        display = self.__color_display() + "_" + self.tank_type
        display = display + " " + self.__direction_display()
        display_destroy = " destroyed" if self.destroyed else ""
        return display + display_destroy

    def __direction_display(self):
        return self.DIRECTION_REF.get(self.direction, "")

    def __color_display(self):
        return 'black' if self.color == 'b' else 'white'

    def copy(self):
        return Tank(self.color, self.tank_type, self.direction)

class KifuLoader:
    DEFAULT_START = {"H1": Tank('w', 'clt', 's'), "H3": Tank('w', 'mt', 's'),
                     "J1": Tank('w', 'mt', 's'), "J3": Tank('w', 'lt', 's'),
                     "F1": Tank('w', 'mt', 's'), "F3": Tank('w', 'lt', 's'),
                     "C1": Tank('w', 'ht', 's'), "C3": Tank('w', 'lt', 's'),
                     "M1": Tank('w', 'ht', 's'), "M3": Tank('w', 'lt', 's'),
                     "I16": Tank('b', 'clt', 'n'), "I14": Tank('b', 'mt', 'n'),
                     "K16": Tank('b', 'mt', 'n'), "K14": Tank('b', 'lt', 'n'),
                     "G16": Tank('b', 'mt', 'n'), "G14": Tank('b', 'lt', 'n'),
                     "D16": Tank('b', 'ht', 'n'), "D14": Tank('b', 'lt', 'n'),
                     "N16": Tank('b', 'ht', 'n'), "N14": Tank('b', 'lt', 'n'),}

    def __init__(self, kifu):
        self.kifu = kifu
        self.tank_positions = [self.DEFAULT_START]
    
    def load(self):
        # render each state of the board for each steps
        pair_actions = self.kifu.record.split("\n")
        for pair_action in pair_actions:
            # example: O8>N10/NW(H10+), K9>K8/SW
            actions = pair_action.split(", ")
            for action in actions:
                # example: O8>N10/NW(H10+)
                self.__process_one_action(action)
        return self.tank_positions

    def __process_one_action(self, action):
        start, end = action.split(">")
        end_xy, end_extra = end.split("/")
        end_direction = end_extra.split("(")[0].lower().strip()
        # needed to handle end_extra: (H10+)
        try:
            extra = end_extra.split("(")[1][:-1]
            special = ('+', '#', '-', '=')
            target = extra
            special = None
            if extra.endswith(special):
                target = extra[:-1]
                special = extra[-2]

        last_position = self.tank_positions[-1]
        new_position = deepcopy(last_position)
        if start:
            # example of moved: O8>N10/NW(H10+)
            tank = last_position.get(start).copy()
            del new_position[start]
        else:
            # example of not moved: >N10/NW(H10+)
            tank = last_position.get(end_xy).copy()
        tank.direction = end_direction
        new_position[end_xy] = tank
        self.tank_positions.append(new_position)
