from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ActivateAccountViewSet
from django.views.generic import TemplateView

router = DefaultRouter()

router.register(r'register',views.register_viewset, basename='register')
router.register(r'login',views.login_viewset,basename='login')
router.register(r'get',views.get_viewset,basename='get')
router.register(r'update',views.update_viewset,basename='update')
router.register(r'delete',views.delete_viewset,basename='delete')
router.register(r'change_password',views.change_password_viewset,basename='change_password')
router.register(r'forget_password',views.forget_password_viewset,basename='forget_password')
router.register(r'varified_otp',views.otp_varification_viewset,basename='varified_otp')



urlpatterns = [
    path('', include(router.urls)),
    path('activate/<str:uid>/<str:token>/', ActivateAccountViewSet.as_view({'get': 'retrieve'}), name='activate-account'),
    # path('CustomUser/activate/<str:uid>/<str:token>/', ActivateAccountViewSet.as_view({'get': 'retrieve'}), name='activate-account'),
    path('account-already-activated/',views.account_already_activated_view,name='account-already-activated') ,
    path('activation-success/', views.activate_success_view,name='activation-success'),
    path('activation-failed',views.activate_failed_view,name='activation-failed')

    
]