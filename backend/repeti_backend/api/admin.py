from django.contrib import admin
from .models import CustomUser, AppSynset, UserList, WordReview, MCQOption  # Import your models

admin.site.register(CustomUser)
admin.site.register(AppSynset)
admin.site.register(UserList)
admin.site.register(WordReview)
admin.site.register(MCQOption)
