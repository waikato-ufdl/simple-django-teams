from django.db import models
from django.conf import settings

from ..mixins import SoftDeleteModel, TeamOwnedModel, SoftDeleteQuerySet
from ..apps import APP_NAME


class MembershipQuerySet(SoftDeleteQuerySet):
    """
    Custom query-set for memberships.
    """
    pass


class Membership(TeamOwnedModel, SoftDeleteModel):
    # Permission constants
    PERMISSION_READ = "R"
    PERMISSION_WRITE = "W"
    PERMISSION_ADMIN = "A"

    # The user whose membership this is
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING,
                             related_name="memberships")

    # The team to which this membership applies
    team = models.ForeignKey(f"{APP_NAME}.Team",
                             on_delete=models.DO_NOTHING,
                             related_name="memberships")

    # The permissions the member has within the team
    permissions = models.CharField(max_length=1,
                                   choices=[
                                       (PERMISSION_READ, "Read"),
                                       (PERMISSION_WRITE, "Write"),
                                       (PERMISSION_ADMIN, "Admin")
                                   ],
                                   default=PERMISSION_READ)

    objects = MembershipQuerySet.as_manager()

    class Meta(TeamOwnedModel.Meta, SoftDeleteModel.Meta):
        constraints = [
            # Ensure that each user is only an active member of each team at most once
            models.UniqueConstraint(name="one_active_membership_per_user_per_team",
                                    fields=["user", "team"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def is_admin(self) -> bool:
        """
        Whether the member is an admin for this team.
        """
        return self.permissions == self.PERMISSION_ADMIN

    def get_owning_team(self):
        return self.team

    def __str__(self) -> str:
        return f"User \"{self.user}\" in team \"{self.team}\""
