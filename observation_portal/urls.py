"""observation_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from observation_portal.requestgroups.viewsets import RequestGroupViewSet, RequestViewSet, DraftRequestGroupViewSet
from observation_portal.userrequests.viewsets import UserRequestViewSet
from observation_portal.blocks.viewsets import PondBlockViewSet
from observation_portal.requestgroups.views import TelescopeStatesView, TelescopeAvailabilityView, AirmassView
from observation_portal.requestgroups.views import InstrumentsInformationView, ObservationPortalLastChangedView
from observation_portal.requestgroups.views import ContentionView, PressureView
from observation_portal.accounts.views import ProfileApiView, MyAuthTokenView
from observation_portal.proposals.viewsets import ProposalViewSet, SemesterViewSet
from observation_portal.observations.views import LastScheduledView
from observation_portal.observations.viewsets import ObservationViewSet, ScheduleViewSet, ConfigurationStatusViewSet
import observation_portal.sciapplications.urls as sciapplications_urls
import observation_portal.requestgroups.urls as requestgroup_urls
import observation_portal.proposals.urls as proposals_urls
import observation_portal.accounts.urls as accounts_urls
import observation_portal.observations.urls as observations_urls
from observation_portal import settings

router = DefaultRouter()
router.register(r'requests', RequestViewSet, 'requests')
router.register(r'requestgroups', RequestGroupViewSet, 'request_groups')
router.register(r'userrequests', UserRequestViewSet, 'userrequests')
router.register(r'blocks', PondBlockViewSet, 'blocks')
router.register(r'drafts', DraftRequestGroupViewSet, 'drafts')
router.register(r'proposals', ProposalViewSet, 'proposals')
router.register(r'semesters', SemesterViewSet, 'semesters')
router.register(r'observations', ObservationViewSet, 'observations')
router.register(r'schedule', ScheduleViewSet, 'schedule')
router.register(r'configurationstatus', ConfigurationStatusViewSet, 'configurationstatus')

api_urlpatterns = ([
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', MyAuthTokenView.as_view(), name='api-token-auth'),
    url(r'^telescope_states/', TelescopeStatesView.as_view(), name='telescope_states'),
    url(r'^telescope_availability/', TelescopeAvailabilityView.as_view(), name='telescope_availability'),
    url(r'profile/', ProfileApiView.as_view(), name='profile'),
    url(r'airmass/', AirmassView.as_view(), name='airmass'),
    url(r'instruments/', InstrumentsInformationView.as_view(), name='instruments_information'),
    url(r'contention/(?P<instrument_type>.+)/', ContentionView.as_view(), name='contention'),
    url(r'pressure/', PressureView.as_view(), name='pressure'),
    url(r'last_changed/', ObservationPortalLastChangedView.as_view(), name='last_changed'),
    url(r'last_scheduled/', LastScheduledView.as_view(), name='last_scheduled')
], 'api')

schema_view = get_schema_view(
    title="Observation Portal API",
    version='2.0',
    description="Test description",
)

redoc_view = TemplateView.as_view(
    template_name='redoc.html',
    extra_context={'schema_url': 'openapi-schema'}
)

urlpatterns = [
    url(r'^', include(requestgroup_urls)),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^api/', include(api_urlpatterns)),
    url(r'^tools/', TemplateView.as_view(template_name='tools.html'), name='tools'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^proposals/', include(proposals_urls)),
    url(r'^observations/', include(observations_urls)),
    url(r'^apply/', include(sciapplications_urls)),
    path('admin/', admin.site.urls),
    url(r'^help/', TemplateView.as_view(template_name='help.html'), name='help'),
    path('openapi', schema_view, name='openapi-schema'),
    path('redoc', redoc_view, name='redoc')
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
