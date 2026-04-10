"""
Translation configurations for incidents models using django-modeltranslation.
"""

from modeltranslation.translator import TranslationOptions, register

from .models import (
    Email,
    Impact,
    PredefinedAnswer,
    Question,
    QuestionCategory,
    SectorRegulation,
    SectorRegulationWorkflowEmail,
    Workflow,
)


@register(Impact)
class ImpactTranslationOptions(TranslationOptions):
    fields = ("label", "headline")


@register(QuestionCategory)
class QuestionCategoryTranslationOptions(TranslationOptions):
    fields = ("label",)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ("label", "tooltip")


@register(PredefinedAnswer)
class PredefinedAnswerTranslationOptions(TranslationOptions):
    fields = ("predefined_answer",)


@register(Email)
class EmailTranslationOptions(TranslationOptions):
    fields = ("subject", "content")


@register(Workflow)
class WorkflowTranslationOptions(TranslationOptions):
    fields = ("label", "description")


@register(SectorRegulation)
class SectorRegulationTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(SectorRegulationWorkflowEmail)
class SectorRegulationWorkflowEmailTranslationOptions(TranslationOptions):
    fields = ("headline",)
