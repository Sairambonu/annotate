# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnnotateDatasets(models.Model):
    sno = models.AutoField(primary_key=True)
    dataset_path = models.TextField()
    language = models.CharField(max_length=20)
    task_name = models.CharField(max_length=50)
    set_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=50)
    deadline = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'annotate_datasets'


class Annotatelanguageusers(models.Model):
    sno = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annotatelanguageusers'
        unique_together = (('email', 'lang'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UserInfo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class UserInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    password = models.TextField()
    email = models.CharField(unique=True, max_length=50)
    role = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    languages = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    last_login = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_info'
