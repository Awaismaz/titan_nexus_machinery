from django.contrib import admin
from django.utils.html import format_html

from . import models


class HeroMetricInline(admin.TabularInline):
    model = models.HeroMetric
    extra = 1


class ValuePropositionInline(admin.TabularInline):
    model = models.ValueProposition
    extra = 1


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [HeroMetricInline, ValuePropositionInline]
    fieldsets = (
        ('Identity', {'fields': ('business_name', 'tagline')}),
        ('Hero', {'fields': ('hero_title', 'hero_subtitle', 'primary_cta_label', 'primary_cta_link', 'secondary_cta_label', 'secondary_cta_link', 'hero_background')}),
        ('About & Experience', {'fields': ('about_title', 'about_body', 'experience_highlight', 'experience_years', 'machines_deployed', 'uptime_commitment', 'response_time')}),
        ('Contact', {'fields': ('contact_email', 'contact_phone', 'whatsapp_link', 'operation_regions', 'support_hours', 'newsletter_blurb', 'promo_video_url', 'footer_statement')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


class MachineImageInline(admin.TabularInline):
    model = models.MachineImage
    extra = 1


class MachineDocumentInline(admin.TabularInline):
    model = models.MachineDocument
    extra = 1


@admin.register(models.Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'availability_status', 'is_featured', 'financing_available')
    list_filter = ('category', 'availability_status', 'is_featured', 'industries')
    search_fields = ('name', 'model_number', 'manufacturer', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('public_id', 'created_at', 'updated_at')
    inlines = [MachineImageInline, MachineDocumentInline]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'industry', 'rating', 'highlight')
    list_filter = ('industry', 'rating', 'highlight')
    search_fields = ('client_name', 'company', 'quote')


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'display_order', 'logo_preview')
    list_editable = ('display_order',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;" />', obj.logo.url)
        return '—'

    logo_preview.short_description = 'Logo'


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order')
    list_editable = ('display_order',)
    list_filter = ('category',)
    search_fields = ('question', 'answer')


@admin.register(models.ServiceOffering)
class ServiceOfferingAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order')
    list_editable = ('display_order',)


class RequestStatusLogInline(admin.TabularInline):
    model = models.RequestStatusLog
    extra = 0
    readonly_fields = ('status', 'comment', 'created_at')


@admin.register(models.CustomRequest)
class CustomRequestAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'company_name', 'machine_type', 'status', 'created_at')
    list_filter = ('status', 'industry', 'created_at')
    search_fields = ('reference_code', 'company_name', 'contact_name', 'machine_type', 'description')
    readonly_fields = ('reference_code', 'created_at', 'updated_at')
    inlines = [RequestStatusLogInline]


@admin.register(models.RequestStatusLog)
class RequestStatusLogAdmin(admin.ModelAdmin):
    list_display = ('custom_request', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('custom_request', 'status', 'comment', 'created_at')


admin.site.site_header = 'Titan Nexus Operations Console'
admin.site.site_title = 'Titan Nexus Admin'
admin.site.index_title = 'Command Center'
