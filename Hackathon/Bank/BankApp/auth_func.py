from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from BankApp.email.send_email import send_email

# Func for 2-way-Auth
def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
# Func for 2-way-Auth
def create_OTP(user, pass_w): # insert pass param
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=True)
    url = device.config_url
    print(url)
    urll = url.split('=')
    qr_code_url = urll[1].replace('&algorithm', '')
    print(f'********* QR-Code: {qr_code_url} *********')
    print(user.email, user.username, pass_w, qr_code_url)

    send_email(user.email, user.username, pass_w, url, qr_code_url)
    return url