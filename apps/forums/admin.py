from django.contrib import admin

from apps.forums.models import Category, Faculty, Forum, Thread, Reply

# Register your models here.
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):

    list_display = ('name', 'short_name', 'date_created')
    
    search_fields = ('name', 'short_name')
    
    list_filter = ('date_created',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'category')
    search_fields = ('title', 'description')
    list_filter = ('faculty', 'category')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'date_created')
    
    search_fields = ('title', 'author__username')
    
    list_filter = ('forum__faculty', 'forum', 'date_created')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'date_created')
    
    search_fields = ('author__username', 'text')