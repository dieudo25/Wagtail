from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel, 
    InlinePanel, 
    PageChooserPanel, 
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

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

class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    
    templates = 'templates/home/home_page.html'

    max_count = 1   # Can only have one instance of home page

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


    # Add field to Wagtail Admin
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ], heading="Banner Options"),
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label='Image'),
        ], heading="Carousel Images"),
        StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['test'] = "HEllo World"
        return render(request, "home/subscribe.html", context)