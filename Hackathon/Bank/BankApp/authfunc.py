from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

# Func for 2-way-Auth
def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

# Func for 2-way-Auth
def create_OTP(user):
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=True)
    url = device.config_url
    #print(url)
    url = url.split('=')
    qr_code_url = url[1].replace('&algorithm', '')
    print(f'********* QR-Code: {qr_code_url} *********')
    return qr_code_url