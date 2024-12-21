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

# Home page view
def webpage(request):
    return render(request, 'index.html')

# Contact page view (with form submission logic)
class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'  # Redirect URL after successful form submission

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

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(contact_form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = context.get('form', None)
        return context

# Admission form view
def admission_view(request):
    if request.method == 'POST':
        admission_form = AdmissionForm(request.POST)
        if admission_form.is_valid():
            # Save form data to the database
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

            return redirect('home')  # Redirect after successful submission
    else:
        admission_form = AdmissionForm()

    return render(request, 'admission_form.html', {'admission_form': admission_form})

# List of all admissions (requires login)
@login_required(login_url='/auth/login/')
def admissionlists(request):
    context = {'all_admissions': Admission.objects.all()}
    return render(request, 'Admissionlist.html', context)

# Contact list view (requires login)
@login_required(login_url='/auth/login/')
def contactlists(request):
    context = {'all_contacts': contactus.objects.all()}
    return render(request, 'Contactlist.html', context)

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

class CourseListView(TemplateView):
    template_name = 'courselist.html'

class CourseListView(TemplateView):
    template_name = 'courselist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = [
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
        return context
class AdmissionFormView(TemplateView):
    template_name = 'admission_form2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve course and duration from the URL parameters
        course_name = self.request.GET.get('course', '')
        course_duration = self.request.GET.get('duration', '')
        context['course_name'] = course_name
        context['course_duration'] = course_duration
        context['form'] = AdForm()  # Provide an empty form on GET request
        return context

    def post(self, request, *args, **kwargs):
        # Initialize form with POST data
        form = AdForm(request.POST)

        # If form is valid, process the data
        if form.is_valid():
            form.save()  # Save the data to the database
            # Add success message and redirect to a success page
            messages.success(request, 'Your admission form has been submitted successfully!')
            return HttpResponseRedirect(reverse('success_page'))  # Redirect to the success page

        # If form is invalid, re-render the form with errors and include the course info
        return render(request, self.template_name, {
            'form': form,
            'course_name': request.POST.get('course', ''),
            'course_duration': request.POST.get('duration', ''),
        })
def success_page(request):
    return render(request, 'success.html')  # Replace 'success.html' with your template
def submit_enrollment(request):
    # Handle the form submission logic here
    if request.method == 'POST':
        # Process form data
        return HttpResponse('Form submitted successfully!')
    return HttpResponse('This is the submit enrollment page.')