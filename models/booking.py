class Booking:
    """One tourist booking of an experience with a guide on a date."""

    def __init__(self, booking_id, tourist_name, group_size, tour_date, language,
                 experience_id, guide_id, total_price, community_share, status,
                 experience_name="", guide_name="", booked_by=""):
        self.booking_id = booking_id
        self.tourist_name = tourist_name
        self.group_size = group_size
        self.tour_date = tour_date
        self.language = language
        self.experience_id = experience_id
        self.guide_id = guide_id
        self.total_price = total_price
        self.community_share = community_share
        self.status = status
        # Extra names, filled in when we read the booking with a JOIN
        self.experience_name = experience_name
        self.guide_name = guide_name
        self.booked_by = booked_by

    def guide_earnings(self):
        """What the guide keeps after the community fund share."""
        return self.total_price - self.community_share
