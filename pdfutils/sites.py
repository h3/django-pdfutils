"""
Taken largely from django.contrib.admin
"""
from functools import update_wrapper
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin import ModelAdmin, actions
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import logout as auth_logout, REDIRECT_FIELD_NAME
from django.contrib.contenttypes import views as contenttype_views
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.conf import settings

from pdfutils.reports import ReportBase, Report

LOGIN_FORM_KEY = 'this_is_the_login_form'


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class ReportSite(object):
    """
    An AdminSite object encapsulates an instance of the Django admin application, ready
    to be hooked in to your URLconf. Models are registered with the AdminSite using the
    register() method, and the get_urls() method can then be used to access Django view
    functions that present a full admin interface for the collection of registered
    models.
    """
    index_template = None

    def __init__(self, name='pdfutils', app_name='report'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name
        self.app_name = app_name

    def register(self, report_or_iterable, **options):
        """
        Registers the given report(s) with the given admin class.

        The report(s) should be report classes, not instances.

        If a report is already registered, this will raise AlreadyRegistered.

        If a report is abstract, this will raise ImproperlyConfigured.
        """
        if issubclass(report_or_iterable, ReportBase):
            report_or_iterable = [report_or_iterable]
        for report in report_or_iterable:
           #if report._meta.abstract:
           #    raise ImproperlyConfigured('The report %s is abstract, so it '
           #          'cannot be registered with pdfutils.' % report.__name__)

            if report in self._registry:
                raise AlreadyRegistered('The report %s is already registered' % report.__name__)

           #if admin_class is not Report and settings.DEBUG:
           #    admin_class.validate(report)

            # Instantiate the admin class to save in the registry
            self._registry[report] = report(**options)

    def unregister(self, report_or_iterable):
        """
        Unregisters the given report(s).

        If a report isn't already registered, this will raise NotRegistered.
        """
        if isinstance(report_or_iterable, Report):
            report_or_iterable = [report_or_iterable]
        for report in report_or_iterable:
            if report not in self._registry:
                raise NotRegistered('The report %s is not registered' % report.__name__)
            del self._registry[report]

    def has_permission(self, request):
        """
        Returns True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def check_dependencies(self):
        """
        Check that all things needed to run the admin have been correctly installed.

        The default implementation checks that LogEntry, ContentType and the
        auth context processor are installed.
        """
        from django.contrib.admin.models import LogEntry
        from django.contrib.contenttypes.models import ContentType

        if not LogEntry._meta.installed:
            raise ImproperlyConfigured("Put 'django.contrib.admin' in your "
                "INSTALLED_APPS setting in order to use the admin application.")
        if not ContentType._meta.installed:
            raise ImproperlyConfigured("Put 'django.contrib.contenttypes' in "
                "your INSTALLED_APPS setting in order to use the admin application.")
        if not ('django.contrib.auth.context_processors.auth' in settings.TEMPLATE_CONTEXT_PROCESSORS or
            'django.core.context_processors.auth' in settings.TEMPLATE_CONTEXT_PROCESSORS):
            raise ImproperlyConfigured("Put 'django.contrib.auth.context_processors.auth' "
                "in your TEMPLATE_CONTEXT_PROCESSORS setting in order to use the admin application.")

    def report_view(self, view, cacheable=False):
        """
        Decorator to create an admin view attached to this ``AdminSite``. This
        wraps the view and provides permission checking by calling
        ``self.has_permission``.

        You'll want to use this from within ``AdminSite.get_urls()``:

            class MyAdminSite(AdminSite):

                def get_urls(self):
                    from django.conf.urls import patterns, url

                    urls = super(MyAdminSite, self).get_urls()
                    urls += patterns('',
                        url(r'^my_view/$', self.report_view(some_view))
                    )
                    return urls

        By default, report_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.
        """
        def inner(request, *args, **kwargs):
            if LOGIN_FORM_KEY in request.POST and request.user.is_authenticated():
                auth_logout(request)
            if not self.has_permission(request):
                if request.path == reverse('admin:logout',
                                           current_app=self.name):
                    index_path = reverse('admin:index', current_app=self.name)
                    return HttpResponseRedirect(index_path)
                return self.login(request)
            return view(request, *args, **kwargs)
        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    @never_cache
    def report(self, request, extra_context=None):
        """
        Render report for the given HttpRequest.

        This should *not* assume the user is already logged in.
        """
        from django.contrib.auth.views import logout
        defaults = {
            'current_app': self.name,
            'extra_context': extra_context or {},
        }
        if self.report_template is not None:
            defaults['template_name'] = self.logout_template
        return logout(request, **defaults)

    def get_urls(self):
        from django.conf.urls import patterns, url, include

        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.report_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns('')

        # Add in each report's views.
        for model_class, model_instance in six.iteritems(self._registry):
            urlpatterns += patterns('',
                url(r'^%s/' % model_instance.slug, model_class.as_view(), 
                    name=model_instance.slug))
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name


# This global object represents the default report site, for the common case.
# You can instantiate ReportSite in your own code to create a custom report site.
site = ReportSite()
