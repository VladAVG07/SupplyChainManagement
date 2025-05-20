from django.core.mail import send_mail
# from django.conf import settings
send_mail(
    'Test Email',
    'This is a test email.',
    'vladgabrielapostol@gmail.com',  # Replace with your email
    ['vlad-gabriel.apostol@asmi.ro'],  # Replace with the recipient's email
    fail_silently=False,
)