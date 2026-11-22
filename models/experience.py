class Experience:
    """A tour experience tourists can book, like a village walk."""

    def __init__(self, experience_id, name, location, price_per_person, duration_hours):
        self.experience_id = experience_id
        self.name = name
        self.location = location
        self.price_per_person = price_per_person
        self.duration_hours = duration_hours

    def price_for(self, group_size):
        """Total price in RWF for a group of this size."""
        return self.price_per_person * group_size
