from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
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


    # Add field to Wagtail Admin
    content_panels = Page.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        ImageChooserPanel('banner_image'),
        PageChooserPanel('banner_cta'),
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"