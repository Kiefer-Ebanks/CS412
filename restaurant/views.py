from django import template
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.


def main(request):
    '''
    Define a view to handle the 'main' request.
    '''

    main_image ="https://robbreport.com/wp-content/uploads/2022/03/The_Barn_Dining_Room_Photo_Credit_Alan_Shortall.jpg"
 
 
    context = {
        "image": main_image
    }
    
    template_name = "restaurant/main.html"
    return render(request, template_name, context)