from django.db import models
from django.contrib.auth import models as modelsAuth


class CustomUser(modelsAuth.AbstractUser):

    birthday = models.DateField(null=True)
    can_be_contacted = models.BooleanField(null=False, default=False)
    data_can_be_shared = models.BooleanField(null=False, default=False)
