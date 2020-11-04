"""Blog page"""

from django.db import models
from django import forms
from django.core.cache import cache
from wagtail.api import APIField
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel, 
    StreamFieldPanel,
    InlinePanel
)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from streams import blocks

from rest_framework.fields import Field


class ImageSerializedField(Field):
    """
        1st Method to render Image field to the API Endpoint with serializer
        Use this method if you need more customization 
    """

    def to_representation(self, value): 
        """ value represente le nom de l'image dans la classe BlogAuthorOrderable
            dans la liste de la variable api_fields du nom author_image
        """ 
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }

class BlogAuthorOrderable(Orderable):
    """Allow us to select one or more blog authors"""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors") #This orderable is attached to BlogDetailPage
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    # Create property to access author informations from the ForeignKey author
    @property
    def author_name(self):
        return self.author.name

    @property
    def author_website(self):
        return self.author.website

    @property
    def author_image(self):
        return self.author.image

    api_fields = [
        APIField("author"),
        APIField("author_name"),
        APIField("author_website"),

        # Render image using D RestFramework serializer
        #APIField("author_image", serializer=ImageSerializedField()),

        # Render image using wagtail ImageRenditionField
        APIField(
            "image_anything", # represente the key used in the API endpoint for the image informations
            serializer=ImageRenditionField(
                'fill-200x250', # Choose the parameter of the image
                source="author_image"
            )               
        ),
    ]



class BlogAuthor(models.Model):
    """Blog author for snippets"""

    name = models.CharField(max_length=50)
    website = models.URLField(max_length=200, blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null = True,
        blank = False,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ], heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ], heading="Links"
        )
    ]

    def __str__(self):
        """String representation of the object"""

        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = 'Blog Authors'
    
register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for a snippet"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        max_length=255,
        allow_unicode=255,
        help_text="A slug to identify posts by this category"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("slug"),
            ], heading="Name and Image",
        ),
    ]

    def __str__(self):
        """String representation of the object"""

        return self.name

    def save(self, *args, **kwargs):

        # Delete automatically the cache where the name of the cache is 
        # blog_post_preview from blog_list_page.html
        key = make_template_fragment_key(
            "blog_category_preview",
            [self.id]
        )
        cache.delete(key)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = 'Blog Categories'
        ordering = ["name"]

register_snippet(BlogCategory)


class BlogListPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = 'blog/blog_list_page.html'

    ajax_template = "blog/blog_list_page_ajax.html"

    max_count = 1 # Nombre maximum de l'objet

    # Limite the child page creation with the one mentionned in the list
    subpage_types = [
        'blog.VideoBlogPage',
        'blog.ArticleBlogPage',
    ]
    
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""

        context = super().get_context(request, *args, **kwargs)
        # "posts" will have child page; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id an subtitle
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at') # post that are published(live()) and have public status(public())
        
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])

        paginator = Paginator(all_posts, 2) # @todo change to 5 per page

        page = request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)


        context["list_page"] = posts
        context["authors"] = BlogAuthor.objects.all()
        context["a_special_link"] = self.reverse_subpage('latest_post')
        context["categories"] = BlogCategory.objects.all()
        return context

    
    @route(r'^year/(\d+)/(\d+)/$', name="blog_by_year")
    def blog_by_year(self, request, year, month):
        context = self.get_context(request)

        print(year)
        print(month)

        # @todo
        # Filter the context to get by year
        return render(request, "blog/latest_posts.html", context)
    
    @route(r'^latest/$', name="latest_post")
    def latest_blog_post(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)

        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')[:3] # latest post that are published(live()) and have public status(public())
        context['list_page'] = all_posts
        return render(request, "blog/latest_posts.html", context)

    @route(r'^category/(?P<cat_slug>[-\w]*)/$', name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on category"""

        context = self.get_context(request)

        # Check if the category exist
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category = None
        
        if category is None:
            # Redirect the user to /blog/
            pass
        
        post_by_category = BlogDetailPage.objects.filter(categories__in=[category])
        paginator = Paginator(post_by_category, 1) # @todo change to 5 per page
        page = request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['list_page'] = posts

        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        # Uncomment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage('latest_post'),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetailPage',
        related_name="tagged_item",
        on_delete=models.CASCADE,
    )


class BlogDetailPage(Page):
    """Parental Blog detail page"""

    parent_page_types = ["blog.BlogListPage"]
    subpage_types = [] # This object (page) can not create child pages
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL
    )
    categories = ParentalManyToManyField("blog.BlogCategory")

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cta", blocks.CTABlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ], heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ], heading="Categories"
        ),
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("content"),
    ]

    api_fields = [
        APIField("blog_authors"),
        APIField("content"),
        # APIField(""),
        # APIField(""),
    ]

    def save(self, *args, **kwargs):

        # Delete automatically the cache where the name of the cache is 
        # blog_post_preview from blog_list_page.html
        key = make_template_fragment_key(
            "blog_post_preview",
            [self.id]
        )
        cache.delete(key)

        return super().save(*args, **kwargs)

# First subclassed blog post page
class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for article"""

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100, 
        blank=True, 
        null=''
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image", 
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Best size for this image will be 1100x400")

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        FieldPanel("subtitle"),
        ImageChooserPanel("intro_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ], heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ], heading="Categories"
        ),
        StreamFieldPanel("content"),
    ]

#Second subclassed blog post page
class VideoBlogPage(BlogDetailPage):
    """A video subclassed blog post page"""

    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=50)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ], heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ], heading="Categories"
        ),
        ImageChooserPanel("banner_image"),
        FieldPanel("youtube_video_id"),
        StreamFieldPanel("content"),
    ]