from django.db import models
from django.contrib.auth.hashers import make_password

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class User(BaseModel):
    user = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return raw_password and make_password(raw_password) == self.password

class ListToDo(BaseModel):
    is_complete = models.BooleanField(default=False)
    task = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.RESTRICT)
    finish_date = models.DateTimeField(blank=True, null=True)
