from django.contrib import admin

from .models import Cooperative, Member, Product
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

from .choices import PRODUCT_TYPES

class MemberInline(admin.TabularInline):
    model = Member
    extra = 1

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ["quantity"]
    
class CooperativeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Renseignements", {"fields": ["coop_name", "coop_phone", "manager"]}),
        ("Produits offerts", {"fields": ["offered_product_1", "offered_product_2", "offered_product_3"]})
    ]
    inlines = [MemberInline]

    search_fields = ["coop_name", "coop_phone"]
    list_display = ["coop_name", "coop_phone", "get_number_members"]
    def get_number_members(self, obj):
        return obj.member_set.count()
    get_number_members.short_description = "Nombre de membre"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(manager=request.user)


class CoopNameListFilter(admin.SimpleListFilter):
    title = _("Coopérative")
    parameter_name = "coop"
    def lookups(self, request, model_admin):
        return [(coop.id, coop.coop_name) for coop in Cooperative.objects.all()]

    def queryset(self, request, queryset):
        if (self.value() == None):
            return queryset
        return queryset.filter(coop__id=self.value())


class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Renseignements", {"fields": ["member_name", "member_phone", "coop", "telegram_id"]})
    ]
    inlines = [ProductInline]

    search_fields = ["member_name", "member_phone", "coop__coop_name"]

    list_display = ["member_name", "member_phone", 'display_coop']
    list_filter = [CoopNameListFilter]

    def display_coop(self, obj):
        link = reverse("admin:pfnl_cooperative_change", args=[obj.coop.id])
        return format_html('<a href="{}">{}</a>', link, obj.coop)

    display_coop.short_description = "Coopérative"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(coop__manager=request.user)
    

    

admin.site.register(Cooperative, CooperativeAdmin)
admin.site.register(Member, MemberAdmin)
# admin.site.register(Product, ProductAdmin)