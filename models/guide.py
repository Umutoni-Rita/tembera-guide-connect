class Guide:
    """A local tour guide of the cooperative."""

    def __init__(self, guide_id, full_name, phone, gender, languages):
        self.guide_id = guide_id
        self.full_name = full_name
        self.phone = phone
        self.gender = gender
        # languages is a list, for example ["EN", "FR"]
        self.languages = languages

    def speaks(self, language):
        """Return True if this guide speaks the given language code."""
        return language in self.languages

    def languages_text(self):
        """Languages as one string for the database, for example 'EN,FR'."""
        return ",".join(self.languages)
