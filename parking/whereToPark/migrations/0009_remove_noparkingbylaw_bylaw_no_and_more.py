# Generated by Django 4.2.2 on 2023-10-06 15:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("whereToPark", "0008_noparkingbylaw_boundary_status_a_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="noparkingbylaw",
            name="bylaw_no",
        ),
        migrations.RemoveField(
            model_name="restrictedparkingbylaw",
            name="bylaw_no",
        ),
    ]