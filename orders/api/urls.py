from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from api.views import PartnerUpdate

app_name = 'backend'
urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
]