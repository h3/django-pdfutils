django-seoutils
===============

A simple django app to generate PDF documents.


Installation
------------

1. In your `settings.py`, add `pdfutils` to your `INSTALLED_APPS`.
   
2. `(r'^reports/', include(pdfutils.site.urls)),` to your `urls.py`
2. Create a `report.py` file in any installed django application.
3. Create your report(s)
4. Profit!


Example report
--------------

Reports are basically views with custom methods and properties.

.. code-block:: django

    # -*- coding: utf-8 -*-

    from django.contrib.auth.models import User
    from django.core.urlresolvers import reverse
    from django.utils.translation import ugettext as _

    from pdfutils.reports import Report
    from pdfutils.sites import site
    from pdfutils.utils import memoize


    class MyUserReport(Report):
        title = _('Users')
        template_name = 'myapp/reports/users-report.html'
        slug = 'users-report'
        orientation = 'portrait'

        @memoize
        def get_users(self):
            """
            This method is not necessary, it is used to showcase the
            memoize decorator which is included in utils. This prevent
            methods from computing their output twice.
            """
            return User.objects.filter(is_staff=True)

        def get_styles(self):
            """
            It is possible to add or override style like so
            """
            self.styles.append('myapp/css/users-report.css')
            return super(AccountStatementReport, self).get_styles()

        def filename(self):
            """
            The filename can be generated dynamically and translated
            """
            return _('Users-report-%(count)s.pdf') % self.get_users().count()

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


Overriding default CSS
----------------------

Since the default CSS (base.css, portrait.css, landscape.css) are normal static files, they can be overrided 
from any other django app which has a `pdfutils` folder in their static folder.


Dependencies
------------

* django >=1.4, < 1.5.99
* decorator == 3.4.0, <= 3.9.9
* PIL == 1.1.7
* reportlab == 2.5
* html5lib == 0.90
* httplib2 == 0.7.4
* pyPdf == 1.13
* xhtml2pdf == 0.0.4
* django-xhtml2pdf == 0.0.3

Note: dependencies are specified in `setup.py`, thus are installed automatically.

Credits
=======

This project was created and is sponsored by:

.. figure:: http://motion-m.ca/media/img/logo.png
    :figwidth: image

Motion Média (http://motion-m.ca)
