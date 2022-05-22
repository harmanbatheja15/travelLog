from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Account, Log, LogImage

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    list_display_links = ('name', 'email')
    readonly_fields = ('id', 'date_joined', 'last_login')
    search_fields = ('date_joined', 'phone', 'name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'message')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page = 10

class LogImageAdmin(admin.StackedInline):
    model = LogImage

class LogAdmin(admin.ModelAdmin):

    def myimage(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.image.url))

    list_display = ('id', 'title', 'location', 'visibility', 'date')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    list_per_page = 10

    inlines = [LogImageAdmin]

    class Meta:
       model = Log

class LogImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Account, AccountAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(LogImage, LogImageAdmin)
