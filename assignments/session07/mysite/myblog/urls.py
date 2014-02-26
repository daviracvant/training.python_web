from django.conf.urls import patterns, url

urlpatterns = patterns('myblog.views',
    url(r'^$',
        'list_view',
        name="blog_index"),
    url(r'^posts/(?P<post_id>\d+)/$',
        'detail_view',
        name="blog_detail"),
    url(r'^post_add/$',
        'post_add',
        name="add post"),

    url(r'^edit_post/(?P<post_id>\d+)/$',
        'post_edit',
        name="edit post"),
)