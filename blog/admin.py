from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('created',)
    list_per_page = 10
    list_max_show_all = 10
    list_select_related = True
    list_display_links = ('title',)
    list_editable = ('slug',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['author']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['title', 'author', 'created', 'updated']
        return ['title', 'author', 'created']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['created', 'updated']
        return ['created']

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ['title', 'content']
        return ['title']

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return {'slug': ('title',)}
        return {}

    def get_raw_id_fields(self, request):
        if request.user.is_superuser:
            return ['author']
        return []

    def get_date_hierarchy(self, request):
        if request.user.is_superuser:
            return 'created'
        return None

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ['created', 'updated']
        return ['created']

    def get_list_per_page(self, request):
        if request.user.is_superuser:
            return 10
        return 5

    def get_list_max_show_all(self, request):
        if request.user.is_superuser:
            return 10
        return 5

    def get_list_select_related(self, request):
        if request.user.is_superuser:
            return True
        return False

    def get_list_editable(self, request):
        if request.user.is_superuser:
            return ['slug']
        return []

