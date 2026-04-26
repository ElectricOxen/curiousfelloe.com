"""Populate new BaseSection fields for the Curious Felloe landing section."""

from django.db import migrations


def populate_sections(apps, schema_editor):
    Section = apps.get_model("landing", "Section")
    Section.objects.update_or_create(
        slug="landing",
        defaults={
            "name": "Landing",
            "section_type": "hero",
            "eyebrow": "An Electric Oxen Company",
            "heading": "Curious Felloe",
            "description": "Indie Games Studio",
            "body": "",
            "content_model": "",
            "display_order": 0,
            "is_hidden": False,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0003_section_background_image_section_body_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_sections, noop),
    ]
