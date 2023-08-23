from django.core.mail import send_mail
import logging, os

logger = logging.getLogger(__name__)

def schedule_email(name, description, send_to_email):
    logger.error('Details: ' + name, description, send_to_email )
    subject =  name + ' ' + 'Forget Me Not Reminder'
    message =  description
    from_email = 'forget.me.no.sei.620@gmail.com'
    try:
        send_mail(
            subject,
            message,
            from_email,
            [send_to_email],
            fail_silently=False,
            auth_user=os.environ['SES_USER'],
            auth_password=os.environ['SES_PW']
        )
    except Exception as e:
        if 'not verified' in e.__str__():
            logger.error("This email is not verified: " + send_to_email)
        else:
            logger.error('An error occurred: %s', e)