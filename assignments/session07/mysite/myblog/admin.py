from django.contrib import admin
from django.core.urlresolvers import reverse
from myblog.models import Post
from myblog.models import Category

#reference: https://docs.djangoproject.com/en/dev/ref/contrib/admin/
class CategoryInline(admin.TabularInline):
    model = Category.posts.through

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]
    #list the date in the display.
    list_display = ( 'title', 'user_link', 'created_date')
    #display the created on and modified on.
    readonly_fields = ('created_date', 'modified_date')
    #add a link to the author.
    def user_link(self, obj):
        return '<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(obj.author.id,)), obj.author)

    user_link.allow_tags = True
    user_link.short_description = 'User'

class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
