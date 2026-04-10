# Generated migration for migrating data from django-parler to django-modeltranslation

from django.db import migrations


PARLER_TABLES = [
    "governanceplatform_sector_translation",
    "governanceplatform_service_translation",
    "governanceplatform_functionality_translation",
    "governanceplatform_operatortype_translation",
    "governanceplatform_regulator_translation",
    "governanceplatform_observer_translation",
    "governanceplatform_regulation_translation",
    "governanceplatform_entitycategory_translation",
]


def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
        [table_name],
    )
    return cursor.fetchone()[0]


def migrate_parler_to_modeltranslation(apps, schema_editor):
    """
    Copy translation data from django-parler tables into django-modeltranslation fields.
    Safe to run even if parler tables no longer exist (they may have been dropped already).
    """
    migrations_config = [
        ("Sector", "governanceplatform_sector_translation", "master", [("name", "name")]),
        ("Service", "governanceplatform_service_translation", "master", [("name", "name")]),
        ("Functionality", "governanceplatform_functionality_translation", "master", [("name", "name")]),
        ("OperatorType", "governanceplatform_operatortype_translation", "master", [("type", "type")]),
        ("Regulator", "governanceplatform_regulator_translation", "master", [
            ("name", "name"),
            ("full_name", "full_name"),
            ("description", "description"),
        ]),
        ("Observer", "governanceplatform_observer_translation", "master", [
            ("name", "name"),
            ("full_name", "full_name"),
            ("description", "description"),
        ]),
        ("Regulation", "governanceplatform_regulation_translation", "master", [("label", "label")]),
        ("EntityCategory", "governanceplatform_entitycategory_translation", "master", [("label", "label")]),
    ]

    language_codes = ["en", "fr", "nl", "de"]

    with schema_editor.connection.cursor() as cursor:
        for model_name, translation_table, parent_fk, field_mappings in migrations_config:
            if not table_exists(cursor, translation_table):
                print(f"Skipping {model_name}: table {translation_table} does not exist")
                continue

            model = apps.get_model("governanceplatform", model_name)
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
        ("governanceplatform", "0061_alter_functionalitytranslation_unique_together_and_more"),
    ]

    operations = [
        migrations.RunPython(
            migrate_parler_to_modeltranslation,
            reverse_migrate_parler_to_modeltranslation,
        ),
    ]
