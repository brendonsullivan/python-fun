"""Saves records of guests and any relations."""


class GuestList:
    """Class for recording guest lists and relations."""

    def __init__(self):
        """Init an empty guestlist."""
        self.guests = set()
        self.relations = dict()
        self.relation_types = {
            'acquaintance': 1,
            'friend': 2,
            'close friend': 3,
            'family': 4,
            'spouse': 5,
        }

    def __str__(self):
        """Return string of guests and relations."""
        return '\n'.join("{a} <-> {b} = {c}".format(
            a=relation[0],
            b=relation[1],
            c=type
        ) for relation, type in self.relations.items())

    def add_relation(self, guest1: str, guest2: str, type: str):
        """Add one relation between pair of guests.
        Guests must both exist already.
        """
        if not (guest1 in self.guests and guest2 in self.guests):
            raise ValueError('Guest not found. Add guest first')

        relation = (min(guest1, guest2), max(guest1, guest2))
        self.relations[relation] = self.relation_types[type]

    def add_guest(self, guest: str):
        """Add a guest."""
        self.guests.add(guest)
