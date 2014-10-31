from django.contrib import admin
from listings.models import Listing, Skill, Category, Major, UserProfile

admin.site.register(Listing)
admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(Major)
admin.site.register(UserProfile)
admin.site.register(Report)



# Register your models here.
