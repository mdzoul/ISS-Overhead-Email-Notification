"""
This code checks if the ISS is visible in the night sky given the user's LATITUDE and LONGITUDE.
It will then send email to alert the user.
"""
from datetime import datetime, timezone
import smtplib
import time
import requests

# To input by user
LATITUDE = 1.352083
LONGITUDE = 103.819839
EMAIL = "user@gmail.com"
PASSWORD = "password"
SMTP_SERVER = {
    "gmail": "smtp.gmail.com",
    "yahoo": "smtp.mail.yahoo.com",
    "hotmail": "smtp-mail.outlook.com",
}


def iss_overheard():
    """Checks if the ISS is within +- 5 degrees of user's location"""
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])

    if LATITUDE - 5 <= iss_latitude <= LATITUDE + 5 \
            and LONGITUDE - 5 <= iss_longitude <= LONGITUDE + 5:
        return True


def nighttime():
    """Returns True if the time now is nighttime (in UTC)"""
    parameters = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0,
    }

    response_sun = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()
    sunrise_hour = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])

    time_now_hour = datetime.now(timezone.utc).hour

    if sunset_hour <= time_now_hour <= sunrise_hour:
        return True


def send_email():
    """Set up to send email to user"""
    # Change the SMTP server in between the ''
    with smtplib.SMTP(f"{SMTP_SERVER['gmail']}") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject:Look up!\n\nThe ISS is above you in the night sky!"
        )


while True:
    time.sleep(60)
    if iss_overheard() and nighttime():
        send_email()
