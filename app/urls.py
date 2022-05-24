from django.urls import path, re_path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticViewSitemap, ProductSitemap
from .forms import LoginForm, UserPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('', views.ProductSneekPeak.as_view(), name='home'),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    # Basic urls
    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='product-detail'),

    path('ram/<slug:data>', views.ram, name='ramdata'),
    path('ram/', views.ram, name='ram'),

    path('solidstatedrive/<slug:data>', views.solidstatedrive, name='solidstatedrivedata'),
    path('solidstatedrive/', views.solidstatedrive, name='solidstatedrive'),
    
    path('harddiskdrive/<slug:data>', views.hdd, name='harddiskdrivedata'),
    path('harddiskdrive/', views.hdd, name='harddiskdrive'),

    path('motherboard/<slug:data>', views.motherboard, name='motherboarddata'),
    path('motherboard/', views.motherboard, name='motherboard'),

    path('keyboard/<slug:data>', views.keyboard, name='keyboarddata'),
    path('keyboard/', views.keyboard, name='keyboard'),

    path('psu/<slug:data>', views.psu, name='psudata'),
    path('psu/', views.psu, name='psu'),

    path('cabinet/<slug:data>', views.cabinet, name='cabinetdata'),
    path('cabinet/', views.cabinet, name='cabinet'),

    path('ups/<slug:data>', views.ups, name='upsdata'),
    path('ups/', views.ups, name='ups'),

    path('pendrive/<slug:data>', views.pendrive, name='pendrivedata'),
    path('pendrive/', views.pendrive, name='pendrive'),

    path('mouse/<slug:data>', views.mouse, name='mousedata'),
    path('mouse/', views.mouse, name='mouse'),


    path('address/', views.AddressView.as_view(), name='address'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Cart urls
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('pluscartitem/', views.plus_cart_item, name='pluscartitem'),
    path('minuscartitem/', views.minus_cart_item, name='minuscartitem'),
    path('removecartitem/', views.remove_cart_item, name='removecartitem'),

    # checkout related
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('buy/<int:pk>', views.buy_now, name='buy-now'),
    path('buynowcheckout/', views.buynowcheckout, name='buynowcheckout'),
    path('buynowpaymentdone/', views.buy_now_payment_done, name='buynowpaymentdone'),
    

    path('orders/', views.orders, name='orders'),

    # url for delete address record
    path('address/<int:id>', views.delete_customer, name='delete_customer'),

    # Auth
    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm, next_page='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Change password
    path('changepasswordsuccess/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/changepasswordsuccess.html'), name='changepasswordsuccess'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',
         form_class=UserPasswordChangeForm, success_url='/changepasswordsuccess/'), name='changepassword'),

    # Reset password
    # path('resetpassword/', auth_views.PasswordResetView.as_view(template_name='app/reset_password.html',
        # form_class=MyPasswordResetForm), name="resetpassword"),
    
    re_path(r'^search/$', views.search, name="search"),

    path("resetpassword/", views.password_reset_request, name="resetpassword"),
    path("password_reset_error/", views.password_reset_error, name="password_reset_error"),
    path('resetpassword/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/reset_password_done.html'), name="password_reset_done"),
    path('resetpasswordconfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/reset_password_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('resetpasswordsuccess', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/reset_password_complete.html'), name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
