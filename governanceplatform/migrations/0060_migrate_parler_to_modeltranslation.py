# Generated migration for migrating data from django-parler to django-modeltranslation

from django.db import migrations


def migrate_parler_to_modeltranslation(apps, schema_editor):
    """
    Migrate translation data from django-parler translation tables to django-modeltranslation fields.

    This migration handles moving data from parler's separate translation tables
    (sector_sectorname, regulator_regulatortranslation, etc.) to the new modeltranslation
    field-suffix pattern (name_en, name_fr, name_nl, name_de).
    """
    # List of models and their translated fields to migrate
    # Format: (model_name, translations_table, parent_field, [(translated_field, field_name)])
    migrations_config = [
        # Governanceplatform models
        ("Sector", "governanceplatform_sectortranslation", "master", [("name", "name")]),
        ("Service", "governanceplatform_servicetranslation", "master", [("name", "name")]),
        ("Functionality", "governanceplatform_functionalitytranslation", "master", [("name", "name")]),
        ("OperatorType", "governanceplatform_operatortypetranslation", "master", [("type", "type")]),
        ("Regulator", "governanceplatform_regulatortranslation", "master", [
            ("name", "name"),
            ("full_name", "full_name"),
            ("description", "description"),
        ]),
        ("Observer", "governanceplatform_observertranslation", "master", [
            ("name", "name"),
            ("full_name", "full_name"),
            ("description", "description"),
        ]),
        ("Regulation", "governanceplatform_regulationtranslation", "master", [("label", "label")]),
        ("EntityCategory", "governanceplatform_entitycategorytranslation", "master", [("label", "label")]),
        # Incidents models
        ("Impact", "incidents_impacttranslation", "master", [("label", "label")]),
        ("QuestionCategory", "incidents_questioncategorytranslation", "master", [("label", "label")]),
        ("Question", "incidents_questiontranslation", "master", [
            ("label", "label"),
            ("tooltip", "tooltip"),
        ]),
        ("PredefinedAnswer", "incidents_predefinedanswertranslation", "master", [
            ("predefined_answer", "predefined_answer"),
        ]),
        ("Email", "incidents_emailtranslation", "master", [
            ("subject", "subject"),
            ("content", "content"),
        ]),
        ("Workflow", "incidents_workflowtranslation", "master", [
            ("label", "label"),
            ("description", "description"),
        ]),
        ("SectorRegulation", "incidents_sectorregulationtranslation", "master", [("name", "name")]),
        ("SectorRegulationWorkflowEmail", "incidents_sectorregulationworkfloweemailtranslation", "master", [
            ("headline", "headline"),
        ]),
    ]

    # Language codes to migrate
    language_codes = ["en", "fr", "nl", "de"]

    # Iterate through each model's translations
    for model_name, translation_table, parent_fk, field_mappings in migrations_config:
        try:
            # Get the model and translation model
            if model_name in ["Impact", "QuestionCategory", "Question", "PredefinedAnswer", "Email", "Workflow", "SectorRegulation", "SectorRegulationWorkflowEmail"]:
                model = apps.get_model("incidents", model_name)
            else:
                model = apps.get_model("governanceplatform", model_name)

            # Get the translation table via raw SQL (parler tables may not be in the ORM)
            with schema_editor.connection.cursor() as cursor:
                for lang_code in language_codes:
                    try:
                        # Query the parler translation table for this language
                        query = f"""
                            SELECT {parent_fk}_id, {', '.join([f'"{mapping[0]}"' for mapping in field_mappings])}
                            FROM {translation_table}
                            WHERE language_code = %s
                        """
                        cursor.execute(query, [lang_code])
                        rows = cursor.fetchall()

                        # Update model instances with translated data
                        for row in rows:
                            instance_id = row[0]
                            try:
                                instance = model.objects.get(pk=instance_id)
                                # Set the translated fields (modeltranslation will create _en, _fr, _nl, _de suffixed fields)
                                for idx, (parler_field, model_field) in enumerate(field_mappings):
                                    field_value = row[idx + 1]
                                    # Set field with language suffix
                                    setattr(instance, f"{model_field}_{lang_code}", field_value)
                                instance.save(update_fields=[f"{mapping[1]}_{lang_code}" for mapping in field_mappings])
                            except model.DoesNotExist:
                                # Instance was deleted, skip
                                pass
                    except Exception as e:
                        # Parler table may not exist for this model, continue
                        print(f"Could not migrate {model_name} for language {lang_code}: {str(e)}")
                        continue
        except Exception as e:
            # Model not found or other error, continue
            print(f"Error migrating {model_name}: {str(e)}")
            continue


def reverse_migrate_parler_to_modeltranslation(apps, schema_editor):
    """
    Reverse migration: Clear modeltranslation fields (data stays in parler tables if they still exist).
    """
    # This is a data migration, reverse is a no-op since we're migrating forward only
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("governanceplatform", "0059_alter_company_country_alter_observer_country_and_more"),
    ]

    operations = [
        migrations.RunPython(
            migrate_parler_to_modeltranslation,
            reverse_migrate_parler_to_modeltranslation,
        ),
    ]
