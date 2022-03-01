from django.contrib import admin
from .models import Event, Category, Feature, Enroll, Review


class EventFilter(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'event_occupancy'

    def lookups(self, request, model_admin):
        filter_list = (
            ('0', '<=50%'),
            ('1', '>50%'),
            ('2', 'sold-out')
        )
        return filter_list

    def queryset(self, request, queryset):
        filter_value = self.value()
        events_id = []
        if filter_value:
            for event in queryset:
                half = event.participants_number / 2
                left = event.participants_number-event.enrolls.count()
                enroll_count = event.enrolls.count()
                if filter_value == '2' and left == 0:
                    events_id.append(event.id)
                elif filter_value == '0' and enroll_count <= left:
                    events_id.append(event.id)
                elif filter_value == '1' and enroll_count > left != 0:
                    events_id.append(event.id)
            return queryset.filter(id__in=events_id)
        else:
            return queryset


class ReviewInstanceInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'event', 'rate', 'text', 'created', 'updated')
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'date_start', 'is_private', 'participants_number',
                    'display_enroll_count', 'display_places_left')
    list_display_links = ('id', 'title')
    list_select_related = ('category',)
    ordering = ('date_start',)
    search_fields = ('title',)
    list_filter = (EventFilter, 'category', 'features')
    readonly_fields = ('id', 'display_enroll_count', 'display_places_left')
    fieldsets = (
        (None, {
            'fields': ('id',)
        }),
        ('Основная информация', {
            'fields': ('title', 'description', 'date_start', 'participants_number',
                       'is_private', 'category', 'features')
        }),
        ('Информация по заявкам', {
            'fields': ('display_enroll_count', 'display_places_left')
        })
    )
    inlines = (ReviewInstanceInline,)
    filter_horizontal = ('features',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_event_count')
    list_display_links = ('id', 'title')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event')
    list_display_links = ('id', 'user', 'event')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event')
    list_display_links = ('id', 'user', 'event')
    list_select_related = ('user', 'event')
    fields = (('id', 'created', 'updated'), 'user', 'event', 'rate', 'text',)
    readonly_fields = ('id', 'created', 'updated')
    list_filter = ('created', 'event')
