# Generated by Django 4.0.5 on 2022-06-14 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0005_task_isdonetoday'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='longestStreak',
            field=models.IntegerField(blank=True, default=0, verbose_name='Longest Streak'),
        ),
    ]
