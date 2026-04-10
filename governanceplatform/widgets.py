from import_export import widgets

from .settings import LANGUAGES


# Custom widget to handle translated M2M relationships
class TranslatedNameM2MWidget(widgets.ManyToManyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()

        names = value.split(self.separator)

        instances = []
        for name in names:
            # With django-modeltranslation, search directly using the field name
            instance = self.model.objects.filter(
                **{self.field: name.strip()},
            ).first()

            if instance is not None:
                instances.append(instance.id)

        return instances


# Custom widget to handle translated ForeignKey relationships
class TranslatedNameWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()

        # With django-modeltranslation, search directly using the field name
        instance = self.model.objects.filter(
            **{self.field: value.strip()},
        ).first()

        if instance is not None:
            return instance
        return
