from enum import Enum


class Direction(Enum):
    OPENED = int("0", 16)
    ESW = int("1", 16)
    NSW = int("2", 16)
    SW = int("3", 16)
    NEW = int("4", 16)
    EW = int("5", 16)
    NW = int("6", 16)
    W = int("7", 16)
    NES = int("8", 16)
    ES = int("9", 16)
    NS = int("A", 16)
    S = int("B", 16)
    NE = int("C", 16)
    E = int("D", 16)
    N = int("E", 16)
    CLOSED = int("F", 16)


    def can_see(self, cardinal_point: 'Direction') -> bool:
        if cardinal_point.value == Direction.S.value:
            return self.value in (Direction.OPENED.value, Direction.S.value, Direction.SW.value, Direction.ES.value, Direction.NES.value, Direction.NSW.value, Direction.NS.value, Direction.ESW.value)
        elif cardinal_point.value == Direction.N.value:
            return self.value in (Direction.OPENED.value, Direction.NES.value, Direction.NEW.value, Direction.NE.value, Direction.NSW.value, Direction.NS.value, Direction.NW.value, Direction.N.value)
        elif cardinal_point.value == Direction.E.value:
            return self.value in (Direction.OPENED.value, Direction.NES.value, Direction.NEW.value, Direction.NE.value, Direction.ESW.value, Direction.ES.value, Direction.EW.value, Direction.E.value)
        elif cardinal_point.value == Direction.W.value:
            return self.value in (Direction.OPENED.value, Direction.NEW.value, Direction.NSW.value, Direction.NW.value, Direction.ESW.value, Direction.EW.value, Direction.SW.value, Direction.W.value)
