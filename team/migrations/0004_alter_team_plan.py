# Generated by Django 5.2.1 on 2025-06-02 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("team", "0003_team_plan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="plan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="team.plan",
            ),
        ),
    ]
