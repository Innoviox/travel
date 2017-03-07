def parseFile(file):
    """Parse a file written as:
    key1, values1
    key2, values2
    key3, values3
    ...
    Into a dictionary."""
    _dict = {}
    with open(file) as f:
        for line in f.read().split("\n"):
            key, *values = line.split(", ")
            _dict[key] = values
    return _dict

_borders = parseFile("america-borders.txt")
_colors = parseFile("america-colors.txt")
_countries = list(_colors.keys())
colors = 'blue', 'red', 'yellow', 'green'
C = 'country'
T = 'transportation'
class Piece():
    def __init__(self, name, _type, color):
        #Type: general type (country/transportation)
        self.name = name
        self.type = _type
        self.color = color

    def __repr__(self):
        return self.name

def createC(name):
    """Quickly create a country object by name"""
    assert name in _borders
    return Piece(name, C, _colors[name])

def createT(_type, color):
    """Create a transportation object by type and color"""
    assert _type in ('plane', 'car')
    return Piece(_type, T, color)

def borders(c1, c2):
    """Checks if c2 borders c1."""
    return c2.name in _borders[c1.name]

def validPlane(c1, c2, plane):
    """Checks if it's a valid plane trip. All arguments must have the same color."""
    return c1.color == plane.color == c2.color

def validCar(c1, c2, car):
    """Checks if c1 borders any country that c2 borders."""
    return any(borders(c1, createC(c)) for c in _borders[c2.name])
    
def check(cards):
    """Checks a set of cards.
       If there are two cards (C -> C), they must a) have different names, and b) border each other.
       Otherwise, there are three cards (C -> T -> C), the countries must have different names, and then checks with a subfunction."""
    print(cards)
    c1, c2 = cards[0], cards[-1]
    if any(c.type != C for c in (c1, c2)):
        return False
    if c1.name == c2.name:
        return False
    if len(cards) == 2:
        if not borders(c1, c2):
            return False
    else:
        t = cards[1]
        if not globals()['valid'+t.name.title()](c1, c2, t):
            return False

    return True

def parse(rack):
    """Returns steps of journey that need to be checked.
    The types of steps are:
        C -> C
        C -> T -> C
    """
    def _parse():
        for index, card in enumerate(rack):
            if index != len(rack) - 1:
                if card.type == T:
                    if index > 0:
                        yield index-1, index, index+1
                else:
                    if card.type == rack[index+1].type == C:
                        yield index, index+1

    return [i for i in set(_parse())]

def valid(rack):
    return rack[0].type==C and \
           rack[-1].type==C and \
           all(check([rack[card] for card in cards]) for cards in parse(rack)) #All steps parse correctly

def createBag():
    bag = [createC(country) for country in _countries]
    bag.extend([createT('plane', color) for _ in range(2) for color in colors])
    bag.extend([createT('car', 'white') for _ in range(5)])
    return bag

