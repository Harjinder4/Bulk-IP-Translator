<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP Geolocation Lookup</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">IP Geolocation Lookup</h1>
        <p class="text-center">This project is a Flask web application that performs IP geolocation lookups. It allows users to input multiple IP addresses, which are then geolocated using the ip-api.com service. The application displays the geolocation results, the top 5 most repeated IPs, and a Google Maps route for the locations.</p>
        
        <h2>Features</h2>
        <ul>
            <li>Bulk IP geolocation lookup using ip-api.com.</li>
            <li>Display of detailed geolocation information including country, city, ISP, latitude, longitude, and more.</li>
            <li>Identification of the top 5 most repeated IPs from the input.</li>
            <li>Generation of a Google Maps route based on the geolocated IP addresses.</li>
            <li>Responsive UI using Bootstrap.</li>
        </ul>

        <h2>Installation</h2>
        <h3>Prerequisites</h3>
        <p>Ensure you have Python 3.x installed. You can download Python from <a href="https://www.python.org/" target="_blank">python.org</a>.</p>
        
        <h3>Steps</h3>
        <ol>
            <li>Clone the repository or download the <code>app.py</code> script.</li>
            <li>Create a virtual environment (recommended) and activate it:</li>
            <pre><code>python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`</code></pre>
            <li>Install the required packages using the <code>requirements.txt</code> file:</li>
            <pre><code>pip install -r requirements.txt</code></pre>
            <li>Run the application:</li>
            <pre><code>python app.py</code></pre>
        </ol>

        <h3>Requirements</h3>
        <p>The required packages are listed in <code>requirements.txt</code>:</p>
        <ul>
            <li>Flask==2.0.1</li>
            <li>requests==2.25.1</li>
            <li>certifi==2021.5.30</li>
        </ul>

        <h2>Usage</h2>
        <ol>
            <li>Navigate to <a href="http://127.0.0.1:5000/" target="_blank">http://127.0.0.1:5000/</a> in your web browser.</li>
            <li>Enter the IP addresses (space-separated) in the provided textarea and submit the form.</li>
            <li>The application will display geolocation results, the top 5 most repeated IPs, and a Google Maps route link if applicable.</li>
        </ol>

        <h2>Code Explanation</h2>
        <h3>Flask Application</h3>
        <p>The Flask application is defined and runs the web server. Routes are defined to handle the main page (<code>'/'</code>) and form submission.</p>

        <h3>IP Lookup and Retry Session</h3>
        <ul>
            <li>The <code>requests_retry_session</code> function ensures reliable HTTP requests with retries.</li>
            <li>The <code>lookup_ip</code> function performs the geolocation lookup for a single IP address using ip-api.com.</li>
            <li>The <code>bulk_lookup</code> function handles the lookup for multiple IP addresses, leveraging threading for performance.</li>
        </ul>

        <h3>Google Maps URL Generation</h3>
        <p>The <code>generate_google_maps_url</code> function creates a Google Maps route URL based on the geolocated IP addresses.</p>

        <h3>HTML Template</h3>
        <p>The HTML template is embedded in the script and uses Bootstrap for styling. The template displays the form, loading bar, geolocation results, top 5 repeated IPs, and Google Maps route link.</p>

        <h2>Note</h2>
        <p>This project was made while I was an intern (Cyber Warrior) in Gurugram under Haryana Police.</p>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>
