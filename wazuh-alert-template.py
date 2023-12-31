#!/var/ossec/framework/python/bin/python3

#Integración de Correo Electrónico para Wazuh
#Autor: Matías Marrero🚀
#Creado en: Septiembre de 2023
#GitHub: https://github.com/Darka94/
#OPENSOURCE WAZUH


import json
import sys
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración SMTP de Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "testing.wazuh.geocom@gmail.com"  # Reemplaza con tu dirección de correo de Gmail
smtp_password = "fgliyctgzonyvhiv"  # Reemplaza con tu contraseña de Gmail

def generate_html(alert):
    """
    Function that generates an HTML-formatted message from the JSON alert.
    """
    description = alert['rule']['description']
    level = alert['rule']['level']
    agentname = alert['agent']['name']
    t = time.strptime(alert['timestamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
    timestamp = time.strftime('%c', t)

    subject = 'Wazuh Alert: {0}, {1}'.format(description, agentname)

    # Genera contenido HTML del mensaje
    html_message = f"""
    <html>
    <head>
      <meta charset="utf-8">
      <title>Wazuh Alert</title>
      <style>
        body {{
          font-family: sans-serif;
          font-size: 16px;
        }}
        h2 {{
          font-size: 24px;
          font-weight: bold;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Wazuh Alert</h2>
        <p>This is an automatic message from your Wazuh Instance.</p>
        <p>On {timestamp}, an event from agent "{agentname}" triggered the rule "{description}" of level {level}.</p>
        <h3>Alert Details:</h3>
        <table>
          <tr>
            <td>Rule</td>
            <td>{description}</td>
          </tr>
          <tr>
            <td>Level</td>
            <td>{level}</td>
          </tr>
          <tr>
            <td>Agent</td>
            <td>{agentname}</td>
          </tr>
          <tr>
            <td>Timestamp</td>
            <td>{timestamp}</td>
          </tr>
        </table>
      </div>
    </body>
    </html>
    """

    return subject, html_message

def main(args):
    """
    Main function. This will call the functions to prepare the message and send the email
    """
    # Read args
    alert_file_location = args[1]
    recipients = args[3]

    # Open the alert file
    with open(alert_file_location, 'r') as alert_file:
        for line in alert_file:
            try:
                # Parse JSON object from each line
                json_alert = json.loads(line)

                # Generating message
                subject, html_message = generate_html(json_alert)

                # Sending message using Gmail SMTP with authentication
                send_email(recipients, subject, html_message)
            except json.decoder.JSONDecodeError as e:
                print("Failed to parse JSON:", str(e))
            except Exception as e:
                print("Error:", str(e))

def send_email(recipients, subject, body):
    """
    Function to send email using authenticated Gmail SMTP server.
    """
    TO = recipients.split(',')

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(TO)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        # SMTP_SSL Example
        mailserver = smtplib.SMTP(smtp_server, smtp_port)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(smtp_username, smtp_password)
        mailserver.sendmail(smtp_username, TO, msg.as_string())
        mailserver.close()
        print('Successfully sent the mail to {}'.format(TO))
    except Exception as e:
        print("Failed to send mail to {}".format(TO))
        print("With error: {}".format(e))

if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 4:
            msg = '{0} {1} {2} {3} {4}'.format(
                time.strftime("%a %b %d %H:%M:%S %Z %Y"),
                sys.argv[1],
                sys.argv[2],
                sys.argv[3],
                sys.argv[4] if len(sys.argv) > 4 else '',
            )
        else:
            msg = '{0} Wrong arguments'.format(time.strftime("%a %b %d %H:%M:%S %Z %Y"))
            bad_arguments = True

        if bad_arguments:
            print("# Exiting: Bad arguments.")
            sys.exit(1)

        # Main function
        main(sys.argv)

    except Exception as e:
        print(str(e))
        raise
