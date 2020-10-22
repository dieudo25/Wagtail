from django.db import models

from wagtail.core.models import Page

class BlogListPage(Page):
    """Listing page lists all the Blog Detail Pages."""
    
    

class BlogDetailPage(Page):
    pass