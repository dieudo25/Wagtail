from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)

from subscribers.models import Subscriber

class SubscriberAdmin(ModelAdmin):
    """"Subscriber admin"""

    model = Subscriber
    menu_label = "Subscribers"
    menu_icon = "placeholder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "full_name",)
    search_fields = ("email", "full_name",)

modeladmin_register(SubscriberAdmin)