from django.shortcuts import render



def homeView(request):
    template_name = 'home.html'
    
    context = {}

    return render(request, template_name, context)


def detailView(request):
    template_name = 'detail_item.html'
    
    context = {}

    return render(request, template_name, context)