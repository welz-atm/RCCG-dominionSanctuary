from django.contrib import admin
from .models import Comment, Service, Photo, Tithe, Donation


class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher',)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('announcer', 'information', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'user',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image',)


class TitheAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount',)


class DonationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'telephone', 'amount', 'status')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tithe, TitheAdmin)
admin.site.register(Donation, DonationAdmin)



