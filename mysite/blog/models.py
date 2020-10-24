"""Blog page"""

from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel, 
    StreamFieldPanel,
    InlinePanel
)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from streams import blocks


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

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = 'Blog Categories'
        ordering = ["name"]

register_snippet(BlogCategory)


class BlogListPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = 'blog/blog_list_page.html'
    
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
        
        paginator = Paginator(all_posts, 1) # @todo change to 5 per page

        page = request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)


        context["posts"] = posts
        context["authors"] = BlogAuthor.objects.all()
        context["a_special_link"] = self.reverse_subpage('latest_post')
        context["categories"] = BlogCategory.objects.all()
        return context

    @route(r'^latest/$', name="latest_post")
    def latest_blog_post(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:3]
        return render(request, "blog/latest_posts.html", context)

    # @route(r'^\?category=(\d+about/)/$', name="blog_category")
    # def post_by_category(self, request, *args, **kwargs):
    #     context = self.get_context(request, *args, **kwargs)
    #     context["categories"] = BlogCategory.objects.filter(name)
    #     return render(request, "blog/latest_posts.html", context)

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

class BlogDetailPage(Page):
    """Parental Blog detail page"""
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