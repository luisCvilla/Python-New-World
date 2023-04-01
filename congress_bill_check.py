import requests
from base64 import BeautifulSoup
import smtplib
import time

# Test
# Set up SMTP server and login credentials
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_address = "your-email-address@gmail.com"
password = "your-email-password"

# URL to the news website you want to scrape
url = "https://www.congress.gov/news/"

# List of bills that have already been seen
seen_bills = []

# Loop indefinitely to continuously check for new bills
while True:

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the articles on the page
    articles = soup.find_all("article")

    # Loop through each article and extract the title and summary
    for article in articles:
        title = article.find("h2").text.strip()
        summary = article.find("p").text.strip()

        # Check if the title includes the word "bill" and if the bill has not been seen before
        if "bill" in title.lower() and title not in seen_bills:
            seen_bills.append(title)

            # Get information on the bill from the Congress.gov API
            bill_id = title.split()[1]
            bill_url = f"https://www.congress.gov/bill/{bill_id}"
            response = requests.get(f"{bill_url}/all-info")
            soup = BeautifulSoup(response.content, "html.parser")
            sponsor = soup.find("div", {"class": "item"}).find("a").text
            cosponsors = [a.text for a in soup.find_all("a", {"class": "member-link"})]

            # Set up the email message with bill information
            message = f"Subject: New Bill Introduced: {title}\n\n{summary}\n\nSponsor: {sponsor}\nCosponsors: {', '.join(cosponsors)}\nBill URL: {bill_url}"

            # Send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_address, password)
                server.sendmail(email_address, email_address, message)

            # Print confirmation
            print("New bill introduced: ", title)

    # Wait for 1 hour before checking again
    time.sleep(3600)
