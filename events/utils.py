from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_registration_email(user_email, event):
    subject = 'Confirmation of Registration'
    from_email = 'onetwoegg@gmail.com'
    recipient_list = [user_email]


    html_message = render_to_string('event_registration_email.html', {'event': event})

    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
