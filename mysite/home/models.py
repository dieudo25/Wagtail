from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.api import APIField
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel, 
    InlinePanel, 
    PageChooserPanel, 
    StreamFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index

from streams import blocks


class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for home âge carousel"""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,      # Home page already exist
        blank=False,    # False = Cannot be blank, True = can be blank
        on_delete=models.SET_NULL,
        related_name="+", # Use the field name
    )

    panels = [
        ImageChooserPanel("carousel_image"),
    ]

    api_fields = [
        APIField("carousel_image")
    ]

class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    
    templates = 'templates/home/home_page.html'

    # Limite the child page creation with the one mentionned in the list
    subpage_types = [
        'blog.BlogListPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ] 

    # The home page can only live under the root page ( another way of limiting creation) 
    parent_page_type = [
        'wagtailcore.Page'
    ]
    # max_count = 1   # Can only have one instance of home page

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,      # Home page already exist
        blank=False,    # False = Cannot be blank, True = can be blank
        on_delete=models.SET_NULL,
        related_name="+", # Use the field name
    )

    # Add link field to another WagTail Page
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,  # True = the button is optional, False = it is required
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    # Add custom field to searchable fields
    search_fields = Page.search_fields + [
        index.SearchField('banner_title', partial_match=True, boost=2),

    ]

    # Add custom fields to API Endpoint
    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta"),
        APIField("carousel_images"),
        APIField("content"),
    ]


    # Add field to Wagtail Admin
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label='Image'),
        ], heading="Carousel Images"),
        StreamFieldPanel("content"),
    ]

    # Hide wagtail default admin tabs
    # promote_panels = []
    # settings_panels = []

    banner_panels = [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ], heading="Banner options"),
    ]

    # Edit wagtail panels
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(banner_panels, heading="Banner settings"), # Add sidebar tab in home page edit
            ObjectList(Page.promote_panels, heading="Promotional Stuff"), # Rename tab in home page edit (promotion)
            ObjectList(Page.settings_panels, heading="Settings Stuff"), # Rename tab in home page edit (settings)
        ]
    )

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['test'] = "HEllo World"
        return render(request, "home/subscribe.html", context)
    
    def get_admin_display_title(self):
        """Set the name of the page displayed in wagtail admin """
        return 'Home page is the best'

# Set verbose name of the field 'title' of the Home Page 
# And change the title of the field in the edit view
# Cette méthode peut être utiliser pour modifier n'importe 
# qu'elle champ et propriété d'un model django
HomePage._meta.get_field("title").verbose_name = "To any verbose name"
HomePage._meta.get_field("title").help_text = "CUSTOM HELP TEXT"
# HomePage._meta.get_field("title").help_text = None #Delete the hlep text

# Set a default value
HomePage._meta.get_field("title").default = "Some Default title for home page"
HomePage._meta.get_field("slug").default = "some-default-title-for-home-page"

