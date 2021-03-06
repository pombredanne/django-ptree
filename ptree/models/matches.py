from django.db import models

class BaseMatch(models.Model):
    """
    Base class for all Matches.
    """

    time_started = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return str(self.pk)

    def is_ready_for_next_participant(self):
        """
        Needs to be implemented by child classes.
        Whether the game is ready for another participant to be added.
        """
        raise NotImplementedError()

    def is_full(self):
        """
        Whether the match is full (i.e. no more ``Participant``s can be assigned).
        """
        return len(self.participants()) >= self.treatment.participants_per_match

    def participants(self):
        return self.participant_set.all()

    class Meta:
        abstract = True
        verbose_name_plural = "matches"

class MatchInTwoPersonAsymmetricGame(BaseMatch):
    participant_1 = models.ForeignKey('Participant',
                                      related_name = "games_as_participant_1",
                                      null=True)
    participant_2 = models.ForeignKey('Participant',
                                      related_name = "games_as_participant_2",
                                      null=True)

    class Meta:
        abstract = True