# admin.py
from django.contrib import admin
from django.utils import timezone
from .models import ServiceRequest

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_type', 'status', 'resolved_at', 'customer')
    list_filter = ('status', 'resolved_at', 'customer')
    search_fields = ('request_type', 'customer__username', 'customer__email')
    readonly_fields = ('resolved_at',)  # Make resolved_at field read-only

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.status == 'Resolved':
            return readonly_fields + ('request_type', 'details', 'attachment', 'status')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.status == 'Resolved' and not obj.resolved_at:
            obj.resolved_at = timezone.now()
        elif obj.status != 'Resolved':
            obj.resolved_at = None
        obj.save()

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status" and not request.user.is_superuser:
            kwargs['choices'] = [('Resolved', 'Resolved')]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

admin.site.register(ServiceRequest, ServiceRequestAdmin)

