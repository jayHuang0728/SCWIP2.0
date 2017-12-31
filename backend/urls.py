from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^list-city/', views.CityListView.as_view()),
    url(r'^list-favorite/', views.FavoriteListOnlyView.as_view()),
    url(r'^del-favorite/(?P<pk>[0-9]+)/$', views.FavoriteDeleteView.as_view()),
    url(r'^add-favorite/(?P<pk>[0-9]+)/$', views.FavoriteAddView.as_view()),
    # url(r'^add-comment/(?P<pk>[0-9]+)/$', views.CommentDetailView.as_view()),
    url(r'^add-comment/(?P<ins_id>[0-9]+)/$', views.CommentDetailView.as_view()),
    # url(r'^8_5/(?P<pk>[0-9]+)/$/$', views.CommentListAll.as_view()),
    url(r'^search-institution/(?P<ins_name>.+)/$', views.InstitutionSearchListView.as_view()),
    url(r'^list-institution/', views.InstitutionListAllView.as_view()),
    url(r'^register/$', views.RegisterView.as_view(), name='rest_register'),
    url(r'^verify-email/$', views.VerifyEmailView.as_view(), name='rest_verify_email'),url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    url(r'^ins_unit_cap-list/(?P<ins_id>[0-9]+)/$', views.InstitutionCapList.as_view()),
    url(r'^list-all-aqi/$', views.AqiListAllView.as_view()),
    # url(r'^6/',
    # url(r'^5/', vie
    url(r'^institution-detail/(?P<pk>[0-9]+)/$', views.InstitutionDetail.as_view()),
    url(r'^list-ins_comment/(?P<ins_id>[0-9]+)/$',views.CommentListView.as_view()),
    url(r'^list-ins_aqi/(?P<ins_id>[0-9]+)/$', views.InstitutionAqiDetailView.as_view()),
    url(r'^list-ins_unit/(?P<ins_id>[0-9]+)/$', views.InstitutionsHasUnitView.as_view()),
    #以下為login
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', views.PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', views.PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^login/$', views.LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', views.LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', views.UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', views.PasswordChangeView.as_view(),
        name='rest_password_change'),


]
