from django.contrib import admin
from .models import Resume,Job

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("user", "file", "short_text")

    def short_text(self, obj):
        # show only first 100 chars of parsed text
        return (obj.text[:100] + "...") if obj.text else "No text parsed"
    short_text.short_description = "Parsed Text"
