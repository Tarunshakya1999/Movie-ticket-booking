from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views import View 
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.pdfgen import canvas
import razorpay
from django.conf import settings
from django.http import Http404

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from uuid import uuid4


from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            
            if associated_users.exists():
                # Create the password reset token and link
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = user.pk
                    reset_link = f"{request.scheme}://{get_current_site(request).domain}/reset/{uid}/{token}/"
                    
                    # Send email with password reset link
                    subject = "Password Reset Request"
                    message = render_to_string("passwordreset.html", {
                        'user': user,
                        'reset_link': reset_link,
                    })
                    send_mail(subject, message, 'shakyatarun32@gmail.com', [email])

                messages.success(request, "Password reset link has been sent to your email.")
                return redirect('password_reset_done')
            else:
                messages.error(request, "No account is associated with this email.")
                return redirect('change-password')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgotpassword.html', {'form': form})


# Home page`s view`
def fun1(request):
    img = ImageCarosel.getimage()  
    category = request.GET.get('category', 'All')
    if category == 'All':
        movies = MoviesModel.objects.all()
        print(movies)
    else:
        movies = MoviesModel.objects.filter(category=category)
    if request.method == 'POST':
            mt = request.POST.get('query')
            if mt != None:
                movies = MoviesModel.objects.filter(title__icontains = mt)
    return render(request, "home.html", {
        'img': img,
        'movies': movies,
        'selected_category': category
    })

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'servicess.html')


def contact_view(request):
    return render(request, "contact.html")

@login_required(login_url='/error2/') 
def movie_details(request,movie_id):
    movie = MoviesModel.objects.get(id=movie_id)
    return render(request,"movie_detail.html",{'movie':movie})
    

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()  # Create an empty form
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, "Congratulations! Registration successful.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
            return render(request, 'registration.html', {'form': form})
        
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Use LoginForm instead of AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()  # Use LoginForm here as well
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home') 


def footer_view(request):
    return render(request, 'footer.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,"profile.html",locals())
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,city=city,state=state,zipcode=zipcode,mobile=mobile,
                           name=name)
            reg.save()
            messages.success(request,"Profile created successfully")
        
        else:
            messages.warning(request,"Profile creation failed")

        return render(request,"profile.html",locals())


class UpdateAddress(View):
    def get(self, request, pk):
        # Get the address object or return 404 if not found
        address = get_object_or_404(Customer, pk=pk)
        
        # Initialize the form with the current address data
        form = CustomerProfileForm(instance=address)
        
        return render(request, "updateprofile.html", {'form': form, 'address': address})

    def post(self, request, pk):
        # Get the address object or return 404 if not found
        address = get_object_or_404(Customer, pk=pk)
        
        # Initialize the form with the POST data and the existing address
        form = CustomerProfileForm(request.POST, instance=address)
        
        if form.is_valid():
            form.save()  # This saves the updated address to the database
            messages.success(request, "Congratulations! Profile Update Successful")
            return redirect('address')  # Redirect to the address list page or wherever you want
        else:
            messages.warning(request, "Invalid Input Data")
        
        # If the form is invalid, re-render the form with error messages
        return render(request, "updateprofile.html", {'form': form, 'address': address})

#Address.html#
@login_required(login_url='/error2/')  # Redirect to error2 
def get(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': add})

# Error2 page view
def error2(request):
    return render(request, 'error2.html')


def book_ticket(request):
    # Capture the movie_name from the URL query parameters
    movie_name = request.GET.get('movie_name', '')

    if request.method == "POST":
        movie_name = request.POST.get("movie_name")
        client_name = request.POST.get("client_name")
        phone_number = request.POST.get("phone_number")
        cinema_hall = request.POST.get("cinema_hall")
        date = request.POST.get("date")
        time = request.POST.get("time")

        seats = int(request.POST.get("seats"))

        # Set a fallback date if not provided
        if not date:
            date = "0000-00-00"  # Default date value

        # Create a movie ticket object in the database
        ticket_id = str(uuid4())  # Generate a unique UUID as ticket_id

        ticket = MovieTickets.objects.create(
            movie_name=movie_name,
            ticket_id=ticket_id,
            client_name=client_name,
            phone_number=phone_number,
            cinema_hall=cinema_hall,
            seats=seats,
            date=date,  # Use the date from the form or fallback to default
            time=time,
           
        )

        # Calculate amount in paise (₹200 per seat)
        amount = seats * 20000  # ₹200 per seat converted to paise
     

        # Razorpay API client setup
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        try:
            # Create an order in Razorpay
            order = client.order.create(dict(
                amount=amount,  # Amount in paise
                currency='INR',
                payment_capture='1',  # Auto capture payment
            ))

            # Get the order ID from Razorpay response
            razorpay_order_id = order['id']

            # Prepare the response with Razorpay order details
            return render(request, "payment.html", {
                "ticket": ticket,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_merchant_key": settings.RAZOR_KEY_ID ,
                "amount": amount,
            })

        except Exception as e:
            # Log error
            print(f"Error occurred: {e}")
            return render(request, "error.html", {"message": str(e)})

    return render(request, "booking.html", {'movie_name': movie_name})


def payment_success(request, ticket_id):
    try:
        ticket = get_object_or_404(MovieTickets, ticket_id=ticket_id)
    except Http404:
        # Optionally handle the error by returning a custom message or redirecting
        return render(request, 'ticket_not_found.html', {'ticket_id': ticket_id})

    # Update the payment status
    ticket.payment_status = True
    ticket.save()

    # Render the ticket details page with the updated ticket information
    return render(request, "ticket.html", {"ticket": ticket})



def download_ticket(request, ticket_id):
    ticket = get_object_or_404(MovieTickets, ticket_id=ticket_id)

    # Prepare the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket_id}.pdf"'

    # Set up the canvas and PDF layout
    p = canvas.Canvas(response, pagesize=letter)

    # Header background and styling
    p.setFillColor(colors.darkblue)
    p.rect(0, 740, 600, 60, fill=True)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(20, 765, "🎟 Movie Ticket")

    # Ticket details section
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.black)

    # Adding some space
    line_height = 20
    y_position = 660  # Shifted lower to accommodate the moved border

    # Ticket information
    p.drawString(100, y_position, f"Movie: {ticket.movie_name}")
    y_position -= line_height
    p.drawString(100, y_position, f"Ticket ID: {ticket.ticket_id}")
    y_position -= line_height
    p.drawString(100, y_position, f"Name: {ticket.client_name}")
    y_position -= line_height
    p.drawString(100, y_position, f"Cinema Hall: {ticket.cinema_hall}")
    y_position -= line_height
    p.drawString(100, y_position, f"Seats: {ticket.seats}")
    y_position -= line_height
    p.drawString(100, y_position, f"Payment Status: {'Paid' if ticket.payment_status else 'Pending'}")

    # Footer section with some branding or footer text
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.grey)
    footer_text = "Thank you for choosing our cinema! Enjoy the movie!"
    p.drawString(100, 100, footer_text)

    # Add a border around the ticket (optional)
    p.setStrokeColor(colors.black)
    p.setLineWidth(2)
    p.rect(20, 520, 560, 180)  # Lowered the border to start at y=520

    # Save the PDF
    p.showPage()
    p.save()

    return response# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def ticket_details(request):
    tickets = MovieTickets.objects.all()  # Get all MovieTickets
    return render(request, "details.html", {"tickets": tickets})

def policies(request):
    return render(request, 'policies.html')

def partners(request):
    partners = Partner.objects.all()  # Fetch all partners from the database
    return render(request, 'partners.html', {'partners': partners})

def ticket_not_found(request):
    return render(request, 'ticket_not_found.html')

def our_legacy(request):
    return render(request, 'legacy.html')


def password_reset_done(request):
    # This view just renders the confirmation page that the email has been sent
    return render(request, 'password_reset_done.html')



