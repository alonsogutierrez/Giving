from django.contrib import admin
from obsequiemos.models import UserProfile, Comment, Gift, Post, Picture, Postulations, DispatchMethod, PostStateType, \
    GiftStateType, GiftDimensionType, UsedTimeType, UserType, SubcategoryGift, CategoryGift, RegionPost, ComunaPost, \
    GiftWeightType, Notifications

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Gift)
admin.site.register(Post)
admin.site.register(Picture)
admin.site.register(Postulations)
admin.site.register(DispatchMethod)
admin.site.register(PostStateType)
admin.site.register(GiftStateType)
admin.site.register(GiftDimensionType)
admin.site.register(UsedTimeType)
admin.site.register(UserType)
admin.site.register(SubcategoryGift)
admin.site.register(CategoryGift)
admin.site.register(RegionPost)
admin.site.register(ComunaPost)
admin.site.register(GiftWeightType)
admin.site.register(Notifications)
