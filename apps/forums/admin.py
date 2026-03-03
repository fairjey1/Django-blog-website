from django.contrib import admin

from apps.forums.models import Faculty, Forum, Thread, Reply

# Register your models here.
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):

    list_display = ('name', 'short_name', 'get_subscriber_count', 'date_created')
    
    search_fields = ('name', 'short_name')
    
    # list_filter: Agrega un panel lateral para filtrar resultados
    list_filter = ('date_created',)

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty')
    search_fields = ('title', 'description')
    list_filter = ('faculty',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'date_created')
    
    search_fields = ('title', 'author__username')
    
    list_filter = ('forum__faculty', 'forum', 'date_created')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'date_created')
    search_fields = ('author__username', 'text')