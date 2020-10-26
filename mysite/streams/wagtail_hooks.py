import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler
)
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_code_styling(features):
    """Add the <code> to the ruchtext editor."""
    
    #1
    # Variables of the feature
    feature_name = "Code"
    type_ = "CODE"
    tag = "code" # html tag

    #2
    # What is show the the Draftail toolbar in admin  
    control = {
        "type": type_,
        "label": "</>",
        "description": "Code"
    } 

    #3
    # Add new features (code) to the draftail editor
    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    #4
    # Convert the html for the db
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    #5 Register
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    #6 Optional
    # Add to all text editor by default
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Creates centered text in our richtext."""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"
    
    control = {
        "type": type_,
        "label": "Center",
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center", # What center the element in wagtail admin  RichTextEditor
        },
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center" #What center the element in the website
                    }
                }
            }
        }
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    
    features.default_features.append(feature_name)
