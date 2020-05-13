from django.conf import settings
from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.QuerySet):
    """
    Base class for query-sets over soft-delete models.
    """
    def active(self):
        """
        Filters the query-set to only those that are active.
        """
        return self.filter(SoftDeleteModel.active_Q)

    def deleted(self):
        """
        Filters the query-set to those that are deleted.
        """
        return self.filter(SoftDeleteModel.deleted_Q)

    def delete(self):
        # Only delete active models
        active = self.active()

        # Perform any pre-delete actions
        active.model.pre_delete_bulk(active)

        # Set the deletion time of the active models
        active.update(deletion_time=now())

    def hard_delete(self):
        """
        Performs a hard-delete of the models.
        """
        # Perform a soft-delete first to trigger pre-delete actions
        self.delete()

        # Hard-delete
        super().delete()


class SoftDeleteModel(models.Model):
    """
    Mixin for models that shouldn't be deleted from the database,
    instead recording a deletion time.
    """
    # The user that created the object
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.DO_NOTHING,
                                related_name="+",
                                editable=False)

    # The creation date/time of the object
    creation_time = models.DateTimeField(auto_now_add=True,
                                         editable=False)

    # The deletion time of the object. A value of null means it hasn't been deleted
    deletion_time = models.DateTimeField(null=True,
                                         default=None,
                                         editable=False)

    # Q object for filtering active and deleted models
    active_Q = models.Q(deletion_time__isnull=True)
    deleted_Q = models.Q(deletion_time__isnull=False)

    # Manager for soft-delete models
    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True
        base_manager_name = default_manager_name = "objects"

    def is_active(self) -> bool:
        """
        Whether the model is still active (not deleted).
        """
        return self.deletion_time is None

    def is_deleted(self) -> bool:
        """
        Whether the model has been deleted.\
        """
        return not self.is_active()

    def pre_delete(self):
        """
        Can be overridden to perform other actions before an instance
        of the model is deleted.
        """
        pass

    @classmethod
    def pre_delete_bulk(cls, query_set):
        """
        Can be overridden to perform other actions before a set
        of models are deleted.

        :param query_set:   The set of objects being deleted.
        """
        pass

    def delete(self, using=None, keep_parents=False):
        # Can't delete the deleted
        if self.is_deleted():
            return

        # Perform pre-delete actions
        self.pre_delete()

        # Set the deletion time
        self.deletion_time = now()

        self.save(update_fields=["deletion_time"])

    def hard_delete(self, using=None, keep_parents=False):
        """
        Hard-deletes this instance.
        """
        # Soft-delete first to trigger any pre-delete actions
        self.delete(using, keep_parents)

        # Hard-delete
        super().delete(using, keep_parents)
