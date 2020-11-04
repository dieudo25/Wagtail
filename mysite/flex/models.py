"""Flexible page"""

from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from wagtail.core import blocks as streamfield_blocks
from streams import blocks


class FlexPage(Page):
    """Flexible page class"""

    template = "flex/flex_page.html"
    parent_page_types = [
        "flex.FlexPage",
        "home.HomePage",
    ]
    subpage_types = [
        "flex.FlexPage",
    ]

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cta", blocks.CTABlock()),
            ("cards", blocks.CardBlock()),
            ("button", blocks.ButtonBlock()),

            # Add a charblock streamfield with oneline og code 
            # it doesn't need to be created in streams/models.py
            ("char_block", streamfield_blocks.CharBlock(
                required=True,
                help_text="Some help text",
                min_length=10,
                max_length=50,
                template="streams/charblock.html"
            )),
        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
