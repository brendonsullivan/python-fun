"""Saves records of guests and any relations."""


class GuestList:
    """Class for recording guest lists and relations."""

    def __init__(self):
        """Init an empty guestlist."""
        self.guests = []
        self.relations = dict()

    def __str__(self):
        """Return string of guests and relations."""
        return '\n'.join("{a} <-> {b} = {c}".format(
            a=relation[0],
            b=relation[1],
            c=type
        ) for relation, type in self.relations.items())

    def __len__(self):
        """Return number of guests."""
        return len(self.guests)

    def __contains__(self, guest):
        """See if guest is in guest list."""
        return guest in self.guests

    def __getitem__(self, key):
        """Return guest # key."""
        return self.guests[key]

    def __iter__(self):
        """Iterate over guests."""
        return self.guests.__iter__()

    def add_guest(self, guest: str):
        """Add a guest."""
        if guest not in self.guests:
            self.guests += [guest]

    def add_relation(self, guest1: str, guest2: str, relation: int):
        """Add one relation between pair of guests.

        Guests must both exist already.
        """
        if not (guest1 in self and guest2 in self):
            raise ValueError('Guest not found. Add guest first')

        edge = (min(guest1, guest2), max(guest1, guest2))
        self.relations[edge] = relation

    def get_relation(self, guest1: str, guest2: str):
        """Return relation for pair of users."""
        if not (guest1 in self and guest2 in self):
            raise ValueError('Guest not found. Add guest first')
        edge = (min(guest1, guest2), max(guest1, guest2))
        return self.relations[edge]
