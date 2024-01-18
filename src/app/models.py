from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User (BaseModel):
	user = models.CharField(max_length=50, blank=False, null=False)
	email = models.EmailField(blank=False, unique=True)
	password = models.CharField(max_length=50, blank=False, null=False)


class ListToDo(BaseModel):
	is_complete = models.BooleanField(default=False)
	task = models.TextField(null=True, blank=True)
	user = models.ForeignKey(User, blank=False, null=False)
	finish_date = models.DateTimeField(blank=True, null=True)

