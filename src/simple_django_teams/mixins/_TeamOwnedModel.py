from django.db import models


class TeamOwnedModel(models.Model):
    """
    Mixin for models whose instances are owned by a particular team.
    """
    def get_owning_team(self):
        """
        Gets the team that owns this object.

        :return:    The team.
        """
        raise NotImplementedError(TeamOwnedModel.get_owning_team.__qualname__)

    class Meta:
        abstract = True
