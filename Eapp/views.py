from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomRegistrationForm, ProductForm
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

from .utils import upload_image_to_imgbb  # Assuming the above function is in utils.py


def ping(request):
    return HttpResponse("Pong")

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    products = Product.objects.filter(product_category='home_kitchen').order_by('-created_at')
    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares
    return render(request, 'home.html', context)

def apparel(request):
    products = Product.objects.filter(product_category='apparel_fashion').order_by('-created_at')
    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares
    return render(request, 'apparel.html', context)

def beauty(request):
    products = Product.objects.filter(product_category='health_beauty').order_by('-created_at')
    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares
    return render(request, 'beauty.html', context)


def computers(request):
    products = Product.objects.filter(product_category='gadgets_computers').order_by('-created_at')

    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares

    return render(request, 'computers.html', context)


def faqs(request):
    return render(request, 'faqs.html')

def food(request):
    products = Product.objects.filter(product_category='food').order_by('-created_at')
    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares
    return render(request, 'food.html',context)

def jewelry(request):
    products = Product.objects.filter(product_category='jewelry_accessories').order_by('-created_at')
    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares
    return render(request, 'jewelry.html', context)


def error(request):
    return render(request, 'error.html')



def vendor(request):
    return render(request, 'vendor.html')


def register(request):
    # If the user is already authenticated
    if request.user.is_authenticated:
        # Retrieve products uploaded by the logged-in user
        user_products = Product.objects.filter(user=request.user)

        # Handle the 'Mark as Sold' action
        if request.method == 'POST' and 'mark_sold' in request.POST:
            product_id = request.POST.get('product_id')
            try:
                product = Product.objects.get(id=product_id, user=request.user)
                product.is_sold = True
                product.save()
                messages.success(request, 'Product marked as sold.')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found or you are not the owner.')

        # Return the user's products to the template
        return render(request, 'register.html', {'user_products': user_products})

    # Handle the registration form submission if the user is not authenticated
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('Eapp:login')  # Redirect to login after successful registration
        else:
            # Loop through the form errors and add them as Django messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomRegistrationForm()

    # Render the registration form if the user is not authenticated
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  # Use Django's built-in login function
            return redirect('Eapp:sell')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')

def index(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'products': products})


CATEGORY_URL_MAPPING = {
    'electronics': 'electronics',
    'home_kitchen': 'home',
    'health_beauty': 'beauty',
    'jewelry_accessories': 'jewelry',
    'apparel_fashion': 'apparel',
    'food': 'food',
    'gadgets_computers': 'computers',
}
@login_required(login_url='Eapp:login')
def sell(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Set the logged-in user

            # Get the uploaded image from the form
            product_image = request.FILES.get('product_image')

            if product_image:
                # Upload the image to ImgBB and get the URL
                image_url = upload_image_to_imgbb(product_image)

                if image_url:
                    # Save the ImgBB image URL in the product
                    product.product_image_url = image_url

            product.save()  # Save the product after updating the image URL
            category = product.product_category  # Get the product category

            # Get the URL slug from the mapping
            category_slug = CATEGORY_URL_MAPPING.get(category, 'Eapp:shop')  # Default to 'shop' if category not found

            messages.success(request, 'Product uploaded successfully! Redirecting in 3 seconds.')

            # Set session flag to show the modal
            request.session['show_share_modal'] = True

            return redirect(f'/{category_slug}')  # Redirect to the category page
        else:
            # If the form is invalid, display an error message
            messages.error(request, 'There was an error with your submission. Please check the details and try again.')
    else:
        form = ProductForm()

    return render(request, 'sell.html', {'form': form})

def electronics(request):
    products = Product.objects.filter(product_category='electronics').order_by('-created_at')
    # Check if the modal should be shown based on session and last shared time
    show_share_modal = request.session.get('show_share_modal', False)
    last_shared_time = request.session.get('last_shared_time')

    # If the last shared time is within 24 hours, don't show the modal
    if last_shared_time and (timezone.now() - last_shared_time) < timedelta(hours=24):
        show_share_modal = False

    context = {
        'products': products,
        'show_share_modal': show_share_modal
    }

    # Remove the session flag after rendering, but only if the user shared on WhatsApp (handled by JS)
    if show_share_modal:
        request.session['show_share_modal'] = True  # Persist modal until user shares
    return render(request, 'electronics.html', context)

def shop(request):
    # Get all products
    products = Product.objects.all().order_by('-created_at')  # Fetch all products from the database
    return render(request, 'shop.html', {'products': products})

@login_required
def update_share_status(request):
    if request.method == 'POST':
        # Update session to mark that the user shared the product
        request.session['last_shared_time'] = timezone.now()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)