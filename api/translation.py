from modeltranslation.translator import register, TranslationOptions

from api.models import Product


@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'address', 'description')