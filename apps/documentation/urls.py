from django.urls import path
from .views import gstdeclaration, bindingagreement, CompanyAvailabilityView , PincodeinfoView, DetectObjectsAndTextView, AttendanceSheet, DirectorList, Minutemeet, RelatedDirectorCompanies, Cindata, GenerateNoticeView, ESOPALLOTMENT, AOA, AMENDEDAOA, BOARDREPORT, noc, partb, trademark, mou
from .utils import Pincode2

urlpatterns = [
    path('attendancesheet', AttendanceSheet, name='attendance-sheet'),
    path('companydirector/<str:cin>', RelatedDirectorCompanies, name='directorinfo'),
    path('companydetails/<str:cin>', Cindata, name='companyinfo'),
    path('gstdeclaration', gstdeclaration, name="gstdeclaration"),
    path('noc', noc, name='noc'),
    path('companyavailability/<str:c_name>/', CompanyAvailabilityView.as_view(), name='check_company_availability'),
    path('pincode/<int:pincode>', PincodeinfoView, name='get_pincode_info'),
    path('pincode2/<int:pincode>', Pincode2, name='get_pincode_info'),
    path('detect', DetectObjectsAndTextView.as_view(), name='detect-objects'),
    path('directorlist', DirectorList.as_view(), name='director-list'),
    path('minutemeet', Minutemeet.as_view(), name='minute-meet'),
    path('noticemeet', GenerateNoticeView.as_view(), name='notice-view'),
    path('esopdata', ESOPALLOTMENT.as_view(), name='esopdetails'),
    path('companyaoa', AOA.as_view(), name='minute_of_aoa'),
    path('amendedaoa', AMENDEDAOA.as_view(), name='company_amended_aoa'),
    path('boardreport', BOARDREPORT.as_view(), name='boardreport'),
    path('partb', partb, name="partb"),
    path('trademark', trademark.as_view(), name="trademark"),
    path('binding', bindingagreement.as_view(), name='binding agreement'),
    path('mou', mou.as_view(), name="mou"),
]