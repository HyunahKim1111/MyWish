from django.contrib import admin
from .models import Post, User

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created_at', 'updated_at']
    raw_id_fields = ['author'] # 회원을 직접 입력해서 찾을 수 있어.
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['content', 'created_at','author__username']
    ordering = ['-updated_at', '-created_at']
admin.site.register(Post, PostAdmin)
admin.site.register(User)

