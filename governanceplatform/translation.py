"""
Translation configurations for governanceplatform models using django-modeltranslation.
"""

from modeltranslation.translator import TranslationOptions, register

from .models import (
    EntityCategory,
    Functionality,
    Observer,
    OperatorType,
    Regulator,
    Regulation,
    Sector,
    Service,
)


@register(Sector)
class SectorTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Functionality)
class FunctionalityTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(OperatorType)
class OperatorTypeTranslationOptions(TranslationOptions):
    fields = ("type",)


@register(Regulator)
class RegulatorTranslationOptions(TranslationOptions):
    fields = ("name", "full_name", "description")


@register(Observer)
class ObserverTranslationOptions(TranslationOptions):
    fields = ("name", "full_name", "description")


@register(Regulation)
class RegulationTranslationOptions(TranslationOptions):
    fields = ("label",)


@register(EntityCategory)
class EntityCategoryTranslationOptions(TranslationOptions):
    fields = ("label",)
