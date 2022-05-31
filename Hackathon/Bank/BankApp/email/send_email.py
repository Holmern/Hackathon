#   https://realpython.com/python-send-email/
#   https://myaccount.google.com/u/2/lesssecureapps?pli=1&rapt=AEjHL4OPIeGvIZrjnZXgSZa2HCc3CZg19CKraN_Hk4xJlQwKw5oxmDwvaKSySdREd4yhs_qMYSxH4fEuzS6eHrTiRMKBYivYag&pageId=none 

import smtplib, ssl
import qrcode
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from .private_info import password, sender_email # REMEMBER TO: Create file called private_info.py in the email folder and create 'sender_email' and 'password' variables and put in your login (to mail that sends emails) info for google to accept

def send_email(receiver_email, usr_name, passwrd, qr_code_url, qr_code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Login credential"
    message["From"] = sender_email
    message["To"] = receiver_email

    print(qr_code_url)
    qr_img_code = qrcode.make(qr_code_url)
    qr_img_code.save('qrcode.jpg')
    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi, your Login is, \nUsername: {usr_name} \nPassword: {passwrd} \nQRCode: {qr_code_url}
    """
    html = f"""\
    <html>
    <body>
        <p>
        Hi, your Login to 3-Way Handshake INC Bank is, 
        <br>Username: {usr_name} \n 
        <br>Password: {passwrd} \n
        <br>
        <br>QRCode to MFA
        <br> <img src="cid:qrcode"></img>
        <br> If QRCode dosen't work use this code: {qr_code}
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # This example assumes the image is in the current directory
    fp = open('qrcode.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<qrcode>')
    message.attach(msgImage)

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f'Mail sent to: {receiver_email}')
        except Exception as ex:
            print(ex, '<--- exception here!')
