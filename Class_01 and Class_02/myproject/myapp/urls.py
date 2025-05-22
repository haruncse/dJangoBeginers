from django.urls import path
from . import views
from . TestView  import test

urlpatterns = [
    path('', views.index, name='index'),  # Example view
    # path('data-acces2', views.dataRender2, name='index2'),  #
    path('data-access3', test.dataRender3, name='index3'),
    path('html1', views.htmlPage, name='html_page2'),  # Example view2
    path('html2', test.htmlPage2, name='html_page3'),  # Example view2

]
