# IP Geolocation Lookup

## Overview

This project is a Flask web application that performs IP geolocation lookups. It allows users to input multiple IP addresses, which are then geolocated using the ip-api.com service. The application displays the geolocation results, the top 5 most repeated IPs, and a Google Maps route for the locations.

## Features

- Bulk IP geolocation lookup using ip-api.com.
- Display of detailed geolocation information including country, city, ISP, latitude, longitude, and more.
- Identification of the top 5 most repeated IPs from the input.
- Generation of a Google Maps route based on the geolocated IP addresses.
- Responsive UI using Bootstrap.

## Installation

### Prerequisites

Ensure you have Python 3.x installed. You can download Python from [python.org](https://www.python.org/).

### Steps

1. Clone the repository or download:
   ```bash
   git clone https://github.com/Harjinder4/Bulk-IP-Translator.git
   cd Bulk-IP-Translator
   ```
2. Create a virtual environment (recommended) and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python main.py
    ```

### Requirements

The required packages are listed in `requirements.txt`:
Flask==2.0.1
requests==2.25.1
certifi==2021.5.30


## Usage

1. Navigate to `http://127.0.0.1:5000/` in your web browser.
2. Enter the IP addresses (space-separated) in the provided textarea and submit the form.
3. The application will display geolocation results, the top 5 most repeated IPs, and a Google Maps route link if applicable.

## Code Explanation

### Flask Application

- The Flask application is defined and runs the web server.
- Routes are defined to handle the main page (`'/'`) and form submission.

### IP Lookup and Retry Session

- The `requests_retry_session` function ensures reliable HTTP requests with retries.
- The `lookup_ip` function performs the geolocation lookup for a single IP address using ip-api.com.
- The `bulk_lookup` function handles the lookup for multiple IP addresses, leveraging threading for performance.

### Google Maps URL Generation

- The `generate_google_maps_url` function creates a Google Maps route URL based on the geolocated IP addresses.

### HTML Template

- The HTML template is embedded in the script and uses Bootstrap for styling.
- The template displays the form, loading bar, geolocation results, top 5 repeated IPs, and Google Maps route link.

### Note

- This project was made while I was an intern (Cyber Warrior) in Gurugram under Haryana Police. 
