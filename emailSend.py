import datetime
import secureProperties
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class emailSend():
    def send_single_email(destinatario, titulo, corpo, title_image, title_image_path, bottom_image, bottom_image_path):
        print(datetime.datetime.now())
        client = boto3.client('ses',region_name=secureProperties.AWS_REGION)
        
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = titulo 
        msg['From'] = secureProperties.SENDER 
        msg['To'] = destinatario

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Encode the text and HTML content and set the character encoding. This step is
        # necessary if you're sending a message with characters outside the ASCII range.
        htmlpart = MIMEText(corpo.encode(secureProperties.CHARSET), 'html', secureProperties.CHARSET)

        # Add the text and HTML parts to the child container.
        msg_body.attach(htmlpart)

        # Define the attachment part and encode it using MIMEApplication.
        title_att = MIMEApplication(open(title_image_path, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        title_att.add_header('Content-Disposition','attachment',filename=title_image)
        title_att.add_header('X-Attachment-Id', '0')
        title_att.add_header('Content-ID', '<0>')

        # Define the attachment part and encode it using MIMEApplication.
        bottom_att = MIMEApplication(open(bottom_image_path, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        bottom_att.add_header('Content-Disposition','attachment',filename=bottom_image)
        bottom_att.add_header('X-Attachment-Id', '1')
        bottom_att.add_header('Content-ID', '<1>')
        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        msg.attach(title_att)
        msg.attach(bottom_att)
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_raw_email(
                Source=secureProperties.SENDER,
                Destinations=[
                        destinatario
                ],
                RawMessage={
                    'Data':msg.as_string(),
                },
                
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            return False
        else:
            print(datetime.datetime.now())
            return True