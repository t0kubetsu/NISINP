from django.db import migrations


def migrate_missing_entities(apps, schema_editor):
    LogReportRead = apps.get_model("incidents", "LogReportRead")

    # Use raw SQL to read from the parler observer translation table.
    # The table may not exist if this migration runs after the parler→modeltranslation
    # schema migration, so we check first and fall back to the modeltranslation column.
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables"
            " WHERE table_name = 'governanceplatform_observer_translation')"
        )
        parler_table_exists = cursor.fetchone()[0]

    for log in LogReportRead.objects.all():
        if (log.entity_name == "" or log.entity_name is None) and log.user is not None:
            user = log.user
            observer = user.observers.first()
            if observer is None:
                continue

            name = None
            with schema_editor.connection.cursor() as cursor:
                if parler_table_exists:
                    # Prefer English, fall back to any available translation
                    cursor.execute(
                        "SELECT name FROM governanceplatform_observer_translation"
                        " WHERE master_id = %s AND language_code = 'en'",
                        [observer.pk],
                    )
                    row = cursor.fetchone()
                    if row is None:
                        cursor.execute(
                            "SELECT name FROM governanceplatform_observer_translation"
                            " WHERE master_id = %s LIMIT 1",
                            [observer.pk],
                        )
                        row = cursor.fetchone()
                    if row:
                        name = row[0]
                else:
                    # parler tables already dropped; read from modeltranslation column
                    cursor.execute(
                        "SELECT name_en FROM governanceplatform_observer WHERE id = %s",
                        [observer.pk],
                    )
                    row = cursor.fetchone()
                    if row:
                        name = row[0]

            if name:
                log.entity_name = name
                log.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("incidents", "0054_incident_incident_last_update"),
    ]

    operations = [
        migrations.RunPython(migrate_missing_entities, migrations.RunPython.noop),
    ]
