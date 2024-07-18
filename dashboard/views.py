
from django.shortcuts import render, redirect, get_object_or_404
from order.models import Order, OrderItem
from store.models import  Writer, Category, Book, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError
from dashboard.forms import BookForm
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from .forms import WriterForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.urls import path
from . import views

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


def admin_required(view_func):
    def wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('store:index')  # Redirect non-admin users to the store app's index
    return wrapped



# Apply the admin_required decorator to restrict access to admin users
@admin_required
def index(request):
    users_count = User.objects.count()
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_writers = Writer.objects.count()
    total_orders = Order.objects.count()
    # Calculate total earnings from paid orders
    total_earnings = Order.objects.filter(paid=True).aggregate(total_earnings=Sum('payable'))['total_earnings'] or 0
    # Calculate the count of unpaid orders
    total_unpaid_orders = Order.objects.filter(paid=False).count()

    unread_messages = Message.objects.filter(read=False).count()
    # Fetch the last 4 messages
    last_4_messages = Message.objects.filter(read=False)[:4]
    # last 4 orders display 
    last_4_orders = Order.objects.all().order_by('-created')[:5]

    paid_orders = Order.objects.filter(paid=True)


  

    # Mark the fetched messages as read
    # for message in last_4_messages:
    #     message.read = True
    #     message.save()

    context = {
    'users_count': users_count,
    'total_books': total_books,
    'total_categories': total_categories,
    'total_writers': total_writers,
    'total_orders': total_orders,
    'total_earnings': total_earnings,
    'total_unpaid_orders': total_unpaid_orders,
    'unread_messages': unread_messages,
    'last_4_messages': last_4_messages,
    'last_4_orders': last_4_orders,
    'paid_orders': paid_orders,

    }

    return render(request, 'index.html', context )

 
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')  # Redirect admin users to the dashboard
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                if request.user.is_staff:  # Check if the logged-in user is an admin
                    return redirect('dashboard:dashboard')  # Redirect admin users to the dashboard
                else:
                    return redirect('store:index')  # Redirect non-admin users to the store app's index
            else:
                messages.error(request, 'Username and password do not match')

    return render(request, "login.html")


def admin_logout(request):
    logout(request)
    return redirect('store:index')	


@admin_required
def all_messages(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})


@admin_required
def mark_messages_as_read(request):
    if request.method == 'POST':
        # Get the message IDs from the request data
        message_ids = request.POST.getlist('message_ids')

        # Update the messages as read
        Message.objects.filter(id__in=message_ids).update(read=True)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@admin_required
def orders(request):
    query = request.GET.get("query")
    orders = Order.objects.all()
    order_items = {}
    for order in orders:
        order_items[order.id] = OrderItem.objects.filter(order=order)
    
    orders = Order.objects.all() 

    # If a query is provided, filter orders by name
    if query:
        orders = orders.filter(Q(name__icontains=query))

    context = {
        'orders': orders,
        'order_items': order_items,
         'query': query, 
    }
    
    return render(request, 'orders.html', context)


@admin_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    # Determine payment status
    payment_status = "Paid" if order.paid else "Unpaid"

    context = {
        'order': order,
        'order_items': order_items,
        'payment_status': payment_status,  
    }

    return render(request, 'order_details.html', context)


# category adding
from .forms import CategoryForm

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:all_categories')  # Redirect to the dashboard or your preferred URL

    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})


# categories List
def categoriesView(request):
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})

# delete a category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('dashboard:all_categories')


def add_writer(request):
    if request.method == 'POST':
        form = WriterForm(request.POST, request.FILES)  # Pass both POST data and files for file fields
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('dashboard:writers')  # Redirect to the list of writers or another appropriate URL
    else:
        form = WriterForm()  # Create a new, empty form instance

    context = {'form': form}
    return render(request, 'add_writers.html', context)

# display writers
def writers(request):
    writers = Writer.objects.all()
    return render(request, 'all_writers.html', {'writers': writers})


# delete writers

def delete_writer(request, writer_id):
    writer = get_object_or_404(Writer, id=writer_id)

    if request.method == 'POST':
        # If a POST request is made (usually from a form submission), delete the writer
        writer.delete()
        return redirect('dashboard:writers')  # Redirect to the writer list page or another appropriate URL after deletion

    # If a GET request is made, display a confirmation page before deletion
    context = {'writer': writer}
    return render(request, 'dashboard/delete_writer.html', context)


@admin_required
def change_payment_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        if payment_status == 'paid' and not order.paid:
            order.paid = True
            order.save()

            # Send email to customer
            subject = 'Payment Confirmation'
            message = f'Thank you for your order. Your payment for Order #{order.id} has been confirmed.'
            from_email = 'muhsinbookstore1.com'  # Your email address
            recipient_list = [order.email]

            email_context = {
                'order': order,
                # Add more context data as needed
            }
            html_message = render_to_string('payment_confirmation_email.html', email_context)

            send_mail(subject, message, from_email, recipient_list, html_message=html_message)

    return redirect('dashboard:orders')




@admin_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:books_list')
    else:
        form = BookForm()

    writers = Writer.objects.all()
    categories = Category.objects.all()

    return render(request, 'add_book.html', {'form': form, 'writers': writers, 'categories': categories})



# this lists the books
@admin_required
def books_list(request):
    books = Book.objects.all()

    query = request.GET.get('query')
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(name__icontains=query) | Q(writer__name__icontains=query)  | Q(category__name__icontains=query)
        )

    context = {
        'books': books,
    }
    return render(request, 'books_list.html', context)


# deletes the books
@admin_required
def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()
    return redirect('dashboard:books_list')

@admin_required
def edit_book(request, book_id):
    # Retrieve the book instance from the database
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # If it's a POST request, process the form data
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # Check if writer and category fields are present in the form data
            # If not, set them to the existing values to avoid changing them
            if 'writer' not in form.cleaned_data:
                form.cleaned_data['writer'] = book.writer
            if 'category' not in form.cleaned_data:
                form.cleaned_data['category'] = book.category
            form.save()
            return redirect('dashboard:books_list')
    else:
        #If it's a GET request, create the form and populate it with initial data
        form = BookForm(instance=book)

    # Retrieve all available writers and categories
    all_writers = Writer.objects.all()
    all_categories = Category.objects.all()

    context = {
        'form': form,
        'book': book,
        'all_writers': all_writers,
        'all_categories': all_categories,
    }

    return render(request, 'edit_book.html', context)



