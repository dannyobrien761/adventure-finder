from django.contrib import admin
from .models import Author
from .models import Post
from .models import Comment, Tag, PostTag
from .models import CollaborateRequest
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status','created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


# Register adventure models.
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(Author)
admin.site.register(Comment)


@admin.register(CollaborateRequest)
class CollaborateRequestAdmin(admin.ModelAdmin):

    list_display = ('message', 'read',)