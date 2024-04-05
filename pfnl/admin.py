from django.contrib import admin

from .models import Cooperative, Member, Product
from django.utils.translation import gettext_lazy as _

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
        ("Renseignements", {"fields": ["coop_name", "coop_phone"]}),
        ("Produits offerts", {"fields": ["offered_product_1", "offered_product_2", "offered_product_3"]})
    ]
    inlines = [MemberInline]
    list_display = ["coop_name", "coop_phone", "get_number_members"]
    def get_number_members(self, obj):
        return obj.member_set.count()
    get_number_members.short_description = "Nombre de membre"

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
        ("Renseignements", {"fields": ["member_name", "member_phone", "coop"]})
    ]
    inlines = [ProductInline]
    list_display = ["member_name", "member_phone", 'get_coop_name']
    list_filter = [CoopNameListFilter]

    def get_coop_name(self, obj):
        return obj.coop.coop_name
    
    get_coop_name.short_description = 'Coopérative'
    

    

admin.site.register(Cooperative, CooperativeAdmin)
admin.site.register(Member, MemberAdmin)
# admin.site.register(Product, ProductAdmin)