# Generated by Django 3.2.5 on 2021-07-23 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangidongi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='events',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='events',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='groups',
        ),
        migrations.AddField(
            model_name='event',
            name='groups',
            field=models.ManyToManyField(related_name='events', to='dangidongi.Group'),
        ),
        migrations.AddField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(related_name='events', to='dangidongi.Profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='people',
            field=models.ManyToManyField(related_name='groups', to='dangidongi.Profile'),
        ),
    ]