django-pdfutils
===============

A simple django app to generate PDF documents.


Installation
------------

1. In your `settings.py`, add `pdfutils` to your `INSTALLED_APPS`.
2. `(r'^reports/', include(pdfutils.site.urls)),` to your `urls.py`
3. Add `pdfutils.autodiscover()` to your `urls.py`
4. Create a `report.py` file in any installed django application.
5. Create your report(s)
6. Profit!

**Note**: If you are using buildout, don't forget to put `pdfutils` 
in your `eggs` section or else the django-pdfutils dependencies wont
be installed.


Example report
--------------

Reports are basically views with custom methods and properties.

.. code-block:: python

    # -*- coding: utf-8 -*-

    from django.contrib.auth.models import User
    from django.core.urlresolvers import reverse
    from django.utils.translation import ugettext as _

    from pdfutils.reports import Report
    from pdfutils.sites import site


    class MyUserReport(Report):
        title = _('Users')
        template_name = 'myapp/reports/users-report.html'
        slug = 'users-report'
        orientation = 'portrait'

        def get_users(self):
            return User.objects.filter(is_staff=True)

        def get_styles(self):
            """
            It is possible to add or override style like so
            """
            self.add_styles('myapp/css/users-report.css')
            return super(AccountStatementReport, self).get_styles()

        def filename(self):
            """
            The filename can be generated dynamically and translated
            """
            return _('Users-report-%(count)s.pdf') % {'count': self.get_users().count() }

        def get_context_data(self):
            """
            Context data is injected just like a normal view
            """
            context = super(AccountStatementReport, self).get_context_data()
            context['user_list'] = self.get_users()
            return context

    site.register(MyUserReport)


The slug should obviously be unique since it is used to build the report URL.

For example, with the default settings and URLs, the URL for report above would be `/reports/users-report/`.

Example template
----------------

.. code-block:: html

    <html>
        <head>
            {{ STYLES|safe }}
        </head>
        <body class="{% if landscape %}landscape{% else %}portrait{% endif %}">
            <ul>
                {% for user in user_list %}
                <li>{{ user }}</li>
                {% endif %}
            </ul>
            <a href="{% url 'pdfutils:your_report_slug' %}?format=html">Add ?format=html for easy template debug</a>
        </body>
    </html>

Some template variables are injected by default in reports:

* title
* slug
* orientation
* MEDIA_URL
* STATIC_URL
* STYLES


Overriding default CSS
----------------------

Since the default CSS (base.css, portrait.css, landscape.css) are normal static files, they can be overrided 
from any other django app which has a `pdfutils` folder in their static folder.

Note: Be sure your applications are listed in the right order in `INSTALLED_APPS` !


Dependencies
------------

* django >=1.4, < 1.5.99
* decorator == 3.4.0, <= 3.9.9
* PIL == 1.1.7
* reportlab == 2.5
* html5lib == 0.90
* httplib2 == 0.9
* pyPdf == 1.13
* xhtml2pdf == 0.0.4
* django-xhtml2pdf == 0.0.3

**Note**: dependencies versions are specified in `setup.py`. The amount of time required to find the right
combination of dependency versions is largely to blame for the creation of this project.
