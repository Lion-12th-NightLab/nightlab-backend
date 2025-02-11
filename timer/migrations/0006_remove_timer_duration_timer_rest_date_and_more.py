# Generated by Django 5.0.7 on 2024-08-02 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("timer", "0005_timer_rest_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="timer",
            name="duration",
        ),
        migrations.AddField(
            model_name="timer",
            name="rest_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="timer",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="timer",
            name="stop_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="timer",
            name="rest_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="timer",
            name="start_time",
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name="timer",
            name="stop_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
