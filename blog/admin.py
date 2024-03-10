from django.contrib import admin
from .models import Post, Author, Tag, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}# we add this extra comma to make it a set 
    list_filter = ("date","author",) # we add this extra comma to make it a set 
    list_display = ("title","date","author",) # we add this extra comma to make it a set 

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name","post_title",)# we can not access the title of post table using post__title in admin.py like views.py if Post had a foreign key to another model like Category, you could access the Category fields using "post__category__name"

    
    def post_title(self, obj):
        return obj.post.title
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)