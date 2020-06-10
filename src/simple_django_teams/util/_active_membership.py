from ._ensure_model import ensure_model, ensure_user_model


def active_membership(user, team):
    """
    Gets the user's membership to the given team,
    if they have one currently.

    :param user:    The user.
    :param team:    The team to get the membership to.
    :return:        The membership.
    """
    # Local imports to avoid circular dependencies
    from ..models import Team, Membership

    # Make sure the user argument is a user
    ensure_user_model(user, False)

    # Make sure the team argument is a team
    ensure_model(team, Team)

    # Get the active memberships between this user and the team
    # (should be zero or one)
    memberships = Membership.objects.active().filter(user=user, team=team)

    # Check the previous condition (very bad if it fails)
    num_memberships: int = len(memberships)
    if num_memberships > 1:
        raise AssertionError(f"Each user should have at most one active membership with "
                             f"a team, but {user} has {num_memberships} with {team}")

    # If no active memberships, return None
    if num_memberships == 0:
        return None

    # Otherwise there is one and only one, so return it
    return memberships[0]
