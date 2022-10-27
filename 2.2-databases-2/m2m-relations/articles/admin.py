from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tag_present = False
        for form in self.forms:
            if form.cleaned_data.get('is_main') and main_tag_present:
                raise ValidationError('Должен остаться только олько один...')
            if form.cleaned_data.get('is_main') and not main_tag_present:
                main_tag_present = True
        if not main_tag_present:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    list_filter = ['title', 'published_at']
    inlines = [ScopeInline, ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
