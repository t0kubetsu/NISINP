# Generated migration for migrating incidents data from django-parler to django-modeltranslation

from django.db import migrations


PARLER_TABLES = [
    "incidents_impact_translation",
    "incidents_questioncategory_translation",
    "incidents_question_translation",
    "incidents_predefinedanswer_translation",
    "incidents_email_translation",
    "incidents_workflow_translation",
    "incidents_sectorregulation_translation",
    "incidents_sectorregulationworkflowemail_translation",
]


def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
        [table_name],
    )
    return cursor.fetchone()[0]


def migrate_parler_to_modeltranslation(apps, schema_editor):
    """
    Copy translation data from django-parler tables into django-modeltranslation fields,
    then drop the parler tables.
    Safe to run even if some parler tables no longer exist.
    """
    migrations_config = [
        ("Impact", "incidents_impact_translation", "master", [
            ("label", "label"),
            ("headline", "headline"),
        ]),
        ("QuestionCategory", "incidents_questioncategory_translation", "master", [
            ("label", "label"),
        ]),
        ("Question", "incidents_question_translation", "master", [
            ("label", "label"),
            ("tooltip", "tooltip"),
        ]),
        ("PredefinedAnswer", "incidents_predefinedanswer_translation", "master", [
            ("predefined_answer", "predefined_answer"),
        ]),
        ("Email", "incidents_email_translation", "master", [
            ("subject", "subject"),
            ("content", "content"),
        ]),
        ("Workflow", "incidents_workflow_translation", "master", [
            ("label", "label"),
            ("description", "description"),
        ]),
        ("SectorRegulation", "incidents_sectorregulation_translation", "master", [
            ("name", "name"),
        ]),
        ("SectorRegulationWorkflowEmail", "incidents_sectorregulationworkflowemail_translation", "master", [
            ("headline", "headline"),
        ]),
    ]

    language_codes = ["en", "fr", "nl", "de"]

    with schema_editor.connection.cursor() as cursor:
        for model_name, translation_table, parent_fk, field_mappings in migrations_config:
            if not table_exists(cursor, translation_table):
                print(f"Skipping {model_name}: table {translation_table} does not exist")
                continue

            model = apps.get_model("incidents", model_name)
            cols = ", ".join([f'"{m[0]}"' for m in field_mappings])

            for lang_code in language_codes:
                cursor.execute(
                    f"SELECT {parent_fk}_id, {cols} FROM {translation_table} WHERE language_code = %s",
                    [lang_code],
                )
                rows = cursor.fetchall()
                for row in rows:
                    instance_id = row[0]
                    try:
                        instance = model.objects.get(pk=instance_id)
                        for idx, (_, model_field) in enumerate(field_mappings):
                            setattr(instance, f"{model_field}_{lang_code}", row[idx + 1])
                        instance.save(
                            update_fields=[f"{m[1]}_{lang_code}" for m in field_mappings]
                        )
                    except model.DoesNotExist:
                        pass

        # Drop parler tables now that data has been copied (or if they were already gone)
        for table in PARLER_TABLES:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")


def reverse_migrate_parler_to_modeltranslation(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    # Run outside a transaction so a missing-table error on one model
    # does not abort the entire connection.
    atomic = False

    dependencies = [
        ("incidents", "0028_alter_impacttranslation_unique_together_and_more"),
    ]

    operations = [
        migrations.RunPython(
            migrate_parler_to_modeltranslation,
            reverse_migrate_parler_to_modeltranslation,
        ),
    ]
