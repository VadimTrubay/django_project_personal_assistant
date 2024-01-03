from .views import main, login_user, create_user_profile, logout_user, ResetPasswordView, terms, activate, success
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


app_name = 'usersapp'

urlpatterns = [
    path('', main, name='main'),

    path('terms/', terms, name='terms'),
    path('login/', login_user, name='login_user'),
    path('signup/', create_user_profile, name='create_user_profile'),
    path('logout/', logout_user, name='logout_user'),
    path('success/', success, name='success'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='usersapp/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='usersapp/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='usersapp/password_reset_complete.html'),
         name='password_reset_complete'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
            activate, name='activate'),
]

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
