from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    current_list = List.objects.get(id=int(list_id))
    return render(request, 'list.html', {'list': current_list})

def new_list(request):
    created_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=created_list)
    return redirect(f'/lists/{created_list.id}')

def add_item(request, list_id):
    Item.objects.create(text=request.POST['item_text'], list=List.objects.get(id=int(list_id)))
    return redirect(f'/lists/{list_id}')
