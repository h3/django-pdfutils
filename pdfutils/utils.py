#-*- coding: utf-8 -*-
import os
import StringIO

from django.conf import settings
from django.template.context import Context
from django.template.loader import get_template

from xhtml2pdf import pisa # TODO: Change this when the lib changes.

"""

The code below is taken from django-xhtml2pdf

https://raw.github.com/chrisglass/django-xhtml2pdf/master/django_xhtml2pdf/utils.py

"""


class UnsupportedMediaPathException(Exception):
    pass


def unique(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    if uri.startswith('http://') or uri.startswith('https://'):
        return uri
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
        if not os.path.exists(path):
            for d in settings.STATICFILES_DIRS:
                path = os.path.join(d, uri.replace(settings.STATIC_URL, ""))
                if os.path.exists(path):
                    break
    else:
        raise UnsupportedMediaPathException(
                                'media urls must start with %s or %s' % (
                                settings.MEDIA_ROOT, settings.STATIC_ROOT))
    return path


def generate_pdf_template_object(template_object, file_object, context):
    """
    Inner function to pass template objects directly instead of passing a filename
    """
    html = template_object.render(Context(context))
    pisa.CreatePDF(html.encode("UTF-8"), file_object , encoding='UTF-8',
                   link_callback=fetch_resources)
    return file_object


def generate_pdf(template_name, file_object=None, context=None): # pragma: no cover
    """
    Uses the xhtml2pdf library to render a PDF to the passed file_object, from the
    given template name.

    This returns the passed-in file object, filled with the actual PDF data.
    In case the passed in file object is none, it will return a StringIO instance.
    """
    if not file_object:
        file_object = StringIO.StringIO()
    if not context:
        context = {}
    tmpl = get_template(template_name)
    generate_pdf_template_object(tmpl, file_object, context)
    return file_object
