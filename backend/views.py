from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Admission, contactus
from .forms import*
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View 
from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
# Home page view
def webpage(request):
    return render(request, 'index.html')

# Contact page view (with form submission logic)
class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'  # Homepage URL after successful form submission

    def form_valid(self, form):
        contact = form.save()

        # Send email to the client (user)
        client_subject = "Thank You for Contacting Us"
        client_message = f"""
        Dear {contact.Full_name},

        Thank you for reaching out to us. We have received your message and will get back to you soon.

        Best regards,
        The Support Team
        """
        client_email = contact.Email
        sender_email = "csesarfraz@gmail.com"
        send_mail(
            subject=client_subject,
            message=client_message,
            from_email=sender_email,
            recipient_list=[client_email],
            fail_silently=False,
        )

        # Send email to the admin
        admin_subject = "New Contact Form Submission"
        admin_email = "csesarfraz@gmail.com"
        admin_context = {
            'full_name': contact.Full_name,
            'email': contact.Email,
            'phone_number': contact.Phone_number,
            'message': contact.Message,
            'timestamp': now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        admin_message = render_to_string('admin_contact_email.html', admin_context)
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=sender_email,
            recipient_list=[admin_email],
            fail_silently=False,
            html_message=admin_message,
        )

        # Render the success message
        return render(self.request, self.template_name, {
            'form_status': 'success',
        })

    def form_invalid(self, form):
        # If form is invalid, render the failure message
        return render(self.request, self.template_name, {
            'form_status': 'failure',
        })
# Admission form view
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .forms import AdmissionForm

def admission_view(request):
    form_status = None
    if request.method == 'POST':
        admission_form = AdmissionForm(request.POST)
        if admission_form.is_valid():
            # Save the form data to the database
            admission = admission_form.save()

            # Send email to the client (user)
            client_subject = "Thank You for Your Admission Submission"
            client_message = f"""
            Dear {admission.full_name},

            Thank you for submitting your admission form for the {admission.course} course.
            We have successfully received your information, and our team will contact you soon.

            Best regards,
            The Team
            """
            client_email = admission.email
            sender_email = "csesarfraz@example.com"
            send_mail(
                client_subject,
                client_message,
                sender_email,
                [client_email],
                fail_silently=False,
            )

            # Send email to the admin
            admin_subject = "New Admission Form Submitted"
            admin_email = "csesarfraz@example.com"
            admin_context = {
                'name': admission.full_name,
                'email': admission.email,
                'phone': admission.phone,
                'course': admission.course,
                'timestamp': now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            admin_message = render_to_string('admin_email_template.html', admin_context)
            send_mail(
                admin_subject,
                admin_message,
                sender_email,
                [admin_email],
                fail_silently=False,
                html_message=admin_message,
            )

            # Success Message
            form_status = 'success'
        else:
            # Failure Message
            form_status = 'failure'
    else:
        admission_form = AdmissionForm()

    return render(request, 'admission_form.html', {'admission_form': admission_form, 'form_status': form_status})


# List of all admissions (requires login)
@login_required(login_url='/auth/login/')
def admissionlists(request):
    context = {'all_admissions': Admission.objects.all()}
    return render(request, 'Admissionlist.html', context)
def download_pdf(request):
    
    admissions = Admission.objects.all()  # Query all admissions
    template_path = 'admissions_pdf_template.html'  # Create a separate template for the PDF

    context = {
        'admissions': admissions,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admissions_list.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')
def admission_admin(request):
    form_status = None  # To hold success/error messages

    if request.method == 'POST':
        admission_form = AdmissionForm(request.POST)
        if admission_form.is_valid():
            # Save the form data to the database
            admission_form.save()
            return redirect('Admissionlist')  # Redirect to the admission list page
        else:
            form_status = 'failure'  # Display error message
    else:
        admission_form = AdmissionForm()  # Blank form for GET request

    # Render the form template for the admin
    return render(request, 'admin_adform.html', {'admission_form': admission_form, 'form_status': form_status})

# Contact list view (requires login)
@login_required(login_url='/auth/login/')
def contactlists(request):
    context = {'all_contacts': contactus.objects.all()}
    return render(request, 'Contactlist.html', context)

def download_contact_pdf(request):
    # Fetch all contact data
    all_contacts = contactus.objects.all()
    template_path = 'contact_list_pdf.html'  # PDF-specific template

    # Context for the template
    context = {
        'all_contacts': all_contacts,
    }

    # Create an HttpResponse for the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contact_list.pdf"'

    # Render the template into HTML
    template = get_template(template_path)
    html = template.render(context)

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check for errors during PDF generation
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')

    return response

# Delete contact (requires login)
@login_required(login_url='/auth/login/')
def deletecontacts(request, id):
    del_contacts = contactus.objects.get(id=id)
    del_contacts.delete()
    return redirect('Contactlist')

# Update contact (requires login)
@login_required(login_url='/auth/login/')
def updatecontacts(request, id):
    up_contacts = get_object_or_404(contactus, id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=up_contacts)
        if form.is_valid():
            form.save()
            return redirect('Contactlist')
    else:
        form = ContactForm(instance=up_contacts)

    return render(request, 'contact.html', {'contact_form': form})

# Update admission (requires login)
@login_required(login_url='/auth/login/')
def updateadmission(request, id):
    admission_to_update = get_object_or_404(Admission, id=id)

    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=admission_to_update)
        if form.is_valid():
            form.save()
            return redirect('Admissionlist')
    else:
        form = AdmissionForm(instance=admission_to_update)

    return render(request, 'updateadmission.html', {'admission_form': form})

# Delete admission (requires login)
@login_required(login_url='/auth/login/')
def deleteadmission(request, id):
    admission_to_delete = Admission.objects.get(id=id)
    admission_to_delete.delete()
    return redirect('Admissionlist')  # Redirect after deletion

# Admin dashboard (requires login)
@login_required(login_url='/auth/login/')
def adminboard(request):
    return render(request, 'admindashboard.html')

# Admission Form View to handle form submission and pre-filled data
class CourseListView(View):
    template_name = 'courselist.html'

    def get(self, request, *args, **kwargs):
        courses = [
            {'name': 'C Programming', 'duration': '1 Month'},
            {'name': 'Python Programming', 'duration': '45 Days'},
            {'name': 'Java Programming', 'duration': '2 Months'},
            {'name': 'Full Stack Development (Python)', 'duration': '3 Months'},
            {'name': 'React JS', 'duration': '1 Month'},
            {'name': 'Front-End Web Development', 'duration': '1.5 Months'},
            {'name': 'AutoCAD', 'duration': '1 Month'},
            {'name': 'Revit', 'duration': '2 Months'},
            {'name': 'Civil 3D', 'duration': '3 Months'},
            {'name': 'Digital Marketing', 'duration': '2 Months'},
            {'name': 'Data Science', 'duration': '4 Months'},
        ]
        return render(request, self.template_name, {'courses': courses})

class AdmissionFormView(View):
    template_name = 'admission_form2.html'

    def get(self, request, *args, **kwargs):
        print(request.POST)
        selected_course = request.GET.get('course', '')
        course_duration = request.GET.get('duration', '')

        # Initialize the form with the selected course if it's provided in the GET parameters
        form = AdmissionForm(initial={'course': selected_course}) 
        return render(request, self.template_name, {
            'form': form,
            'course_name': selected_course,
            'course_duration': course_duration,
        })

    def post(self, request, *args, **kwargs):
        selected_course = request.GET.get('course', '') 
        course_duration = request.GET.get('duration', '')

        # Ensure that the 'course' field is included in the POST data
        if selected_course:
            request.POST = request.POST.copy() 
            request.POST['course'] = selected_course 

        form = AdmissionForm(request.POST)

        if form.is_valid():
            # Save form data to the database
            admission = form.save()

            # Send email to the client (user)
            client_subject = "Thank You for Your Admission Submission"
            client_message = f"""
            Dear {admission.full_name},

            Thank you for submitting your admission form for the {admission.course} course.
            We have successfully received your information, and our team will contact you soon.

            Best regards,
            The Team
            """
            client_email = admission.email
            sender_email = "csesarfraz@example.com"
            send_mail(
                client_subject,
                client_message,
                sender_email,
                [client_email],
                fail_silently=False,
            )

            # Send email to the admin
            admin_subject = "New Admission Form Submitted"
            admin_email = "csesarfraz@example.com"
            admin_context = {
                'name': admission.full_name,
                'email': admission.email,
                'phone': admission.phone,
                'course': admission.course,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            admin_message = render_to_string('admin_email_template.html', admin_context)
            send_mail(
                admin_subject,
                admin_message,
                sender_email,
                [admin_email],
                fail_silently=False,
                html_message=admin_message,
            )

            # Display success message and redirect
            messages.success(request, "Your admission form has been successfully submitted!")
            return redirect('home') 

        else:
            return render(request, self.template_name, {
                'form': form,
                'course_name': selected_course,
                'course_duration': course_duration,
            })