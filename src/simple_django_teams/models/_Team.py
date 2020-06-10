from django.conf import settings
from django.db import models

from ..apps import APP_NAME
from ..mixins import TeamOwnedModel, SoftDeleteModel, SoftDeleteQuerySet
from ..util import ensure_user_model


class TeamQuerySet(SoftDeleteQuerySet):
    """
    Custom query-set for teams, which can filter results to
    those that a given user has admin access to.
    """
    def user_is_admin_for(self, user):
        """
        Filters the teams to those the given user is an
        admin for.

        :param user:    The user.
        :return:        The teams.
        """
        # Local import to avoid circular references
        from ._Membership import Membership

        # Make sure we are passed a user model
        ensure_user_model(user)

        # Unauthenticated users can't be admins
        if not user.is_authenticated:
            return self.none()

        # Superusers/staff are honourary admins for all teams
        if user.is_superuser or user.is_staff:
            return self.all()

        return self.filter(memberships__permissions=Membership.PERMISSION_ADMIN,
                           memberships__deletion_time__isnull=True,
                           memberships__user=user)


class Team(TeamOwnedModel, SoftDeleteModel):
    """
    A team represents a collection of users.
    """
    # The name of the team
    name = models.CharField(max_length=200)

    # The members of the team
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through=f"{APP_NAME}.Membership",
                                     through_fields=("team", "user"),
                                     related_name="teams")

    objects = TeamQuerySet.as_manager()

    class Meta(SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each active team has a unique name
            models.UniqueConstraint(name="unique_active_team_names",
                                    fields=["name"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def active_members(self):
        """
        Gets the query-set of active members of this team.

        :return:    The query-set of active members (users).
        """
        from ._Membership import Membership

        return self.members.filter(memberships__in=Membership.objects.active())

    def get_owning_team(self):
        return self

    def pre_delete(self):
        # Delete the memberships to this team
        self.memberships.all().delete()

    @classmethod
    def pre_delete_bulk(cls, query_set):
        # Delete the memberships to this team
        from ._Membership import Membership
        Membership.objects.filter(team__in=query_set).delete()

    def __str__(self) -> str:
        return self.name
