from flask import Flask, request, render_template_string
import requests
import json
import certifi
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry # type: ignore

app = Flask(__name__)

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

def lookup_ip(ip):
    """Using ip-api.com."""
    base_url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests_retry_session().get(base_url, verify=certifi.where())
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                return {
                    "ip": ip,
                    "country_name": data["country"],
                    "city": data.get("city", "N/A"),
                    "latitude": data.get("lat", "N/A"),
                    "longitude": data.get("lon", "N/A"),
                    "isp": data.get("isp", "N/A"),
                    "continent": data.get("continent", "N/A"),
                    "continent_code": data.get("continentCode", "N/A"),
                    "country_code": data.get("countryCode", "N/A"),
                    "region": data.get("region", "N/A"),
                    "region_name": data.get("regionName", "N/A"),
                    "district": data.get("district", "N/A"),
                    "zip": data.get("zip", "N/A"),
                    "timezone": data.get("timezone", "N/A"),
                    "offset": data.get("offset", "N/A"),
                    "currency": data.get("currency", "N/A"),
                    "org": data.get("org", "N/A"),
                    "as": data.get("as", "N/A"),
                    "asname": data.get("asname", "N/A"),
                    "mobile": data.get("mobile", False),
                    "proxy": data.get("proxy", False),
                    "hosting": data.get("hosting", False),
                }
            else:
                print(f"Error for IP {ip}: {data.get('message', 'No message')}")
        else:
            print(f"Error: HTTP status {response.status_code} for IP {ip}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException for IP {ip}: {e}")
    return None


def bulk_lookup(ips):
    ip_counts = Counter(ips)
    unique_ips = list(ip_counts.keys())
   
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(lookup_ip, ip) for ip in unique_ips]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    
    # top 5 most repeated IPs
    top_5_ips = ip_counts.most_common(5)
    
    return results, top_5_ips

def generate_google_maps_url(locations):
    if len(locations) < 2:
        return None
    
    base_url = "https://www.google.com/maps/dir/?api=1"
    origin = f"{locations[0]['latitude']},{locations[0]['longitude']}"
    destination = f"{locations[-1]['latitude']},{locations[-1]['longitude']}"
    
    if len(locations) == 2:
        map_url = f"{base_url}&origin={origin}&destination={destination}"
    else:
        waypoints = [f"{loc['latitude']},{loc['longitude']}" for loc in locations[1:-1]]
        waypoints_param = "|".join(waypoints)
        map_url = f"{base_url}&origin={origin}&destination={destination}&waypoints={waypoints_param}"
    
    return map_url

# HTML template
html_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>IP Geolocation Lookup</title>
  <!-- Bootstrap CSS -->
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #f8f9fa;
      padding-top: 20px;
    }
    .container {
      max-width: 800px;
      margin: auto;
      background-color: #ffffff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h1, h2 {
      color: #007bff;
      text-align: center;
    }
    form {
      margin-bottom: 20px;
    }
    .btn-primary {
      background-color: #007bff;
      border-color: #007bff;
    }
    .btn-primary:hover {
      background-color: #0056b3;
      border-color: #0056b3;
    }
    .list-group-item {
      background-color: #f0f0f0;
      margin-bottom: 10px;
      border-color: #d0d0d0;
    }
    .list-group-item:last-child {
      margin-bottom: 0;
    }
    .progress {
      height: 30px;
    }
    .progress-bar {
      line-height: 30px;
    }
    .additional-info {
      display: none;
    }
    .img-fluid{
    height: 211px;
    width:248px;
    }
  </style>
  <script>
    function showLoading() {
      document.getElementById('loading-bar').style.display = 'block';
    }

    function toggleAdditionalInfo(id) {
      var info = document.getElementById(id);
      if (info.style.display === 'none') {
        info.style.display = 'block';
      } else {
        info.style.display = 'none';
      }
    }
  </script>
</head>
<body>
  <div class="container">
    <img src="https://seeklogo.com/myaccount/myuploadsimages/haryana-police_ABBAB2F37F.png" alt="Logo" class="img-fluid mx-auto d-block"  style="max-width: 2000px; margin-bottom: 8px;">
    <h1>IP Geolocation Lookup</h1>
    <form method="post" onsubmit="showLoading()">
      <div class="form-group">
        <label for="ipsInput">Enter your IPs (space separated):</label>
        <textarea class="form-control" id="ipsInput" name="ipsInput" rows="5" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <div id="loading-bar" style="display: none;">
      <div class="progress">
        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%;">Loading...</div>
      </div>
    </div>
    {% if locations %}
    {% if map_url %}
    <div class="card mt-3">
      <div class="card-body">
        <h2>Google Maps Route:</h2>
        <a href="{{ map_url }}" target="_blank" class="btn btn-primary">View Route on Google Maps</a>
      </div>
    </div>
    {% else %}
    <p class="text-danger mt-3">Cannot generate Google Maps route because there are insufficient locations.</p>
    {% endif %}
    {% if top_5_ips %}
    <div class="card mt-3">
      <div class="card-body">
        <h2>Top 5 Most Repeated IPs:</h2>
        <ul class="list-group">
          {% for ip, count in top_5_ips %}
          <li class="list-group-item">
            <strong>IP:</strong> {{ ip }}<br>
            <strong>Count:</strong> {{ count }}
          </li>
          {% endfor %}
        </ul>
      </div>
    </div>
    {% endif %}
    <div class="card mt-3">
      <div class="card-body">
        <h2>Geolocation Results:</h2>
        <ul class="list-group">
          {% for location in locations %}
          <li class="list-group-item">
            <strong>IP:</strong> {{ location.ip }}<br>
            <strong>ISP:</strong> {{ location.isp }}<br>
            <a href="javascript:void(0);" onclick="toggleAdditionalInfo('info-{{ loop.index }}')">Read more</a>
            <div class="additional-info" id="info-{{ loop.index }}">
              <strong>Country:</strong> {{ location.country_name }}<br>
              <strong>City:</strong> {{ location.city }}<br>
              <strong>Latitude:</strong> {{ location.latitude }}<br>
              <strong>Longitude:</strong> {{ location.longitude }}<br>
              <strong>Continent:</strong> {{ location.continent }}<br>
              <strong>Continent Code:</strong> {{ location.continent_code }}<br>
              <strong>Country Code:</strong> {{ location.country_code }}<br>
              <strong>Region:</strong> {{ location.region }}<br>
              <strong>Region Name:</strong> {{ location.region_name }}<br>
              <strong>District:</strong> {{ location.district }}<br>
              <strong>Zip:</strong> {{ location.zip }}<br>
              <strong>Timezone:</strong> {{ location.timezone }}<br>
              <strong>Offset:</strong> {{ location.offset }}<br>
              <strong>Currency:</strong> {{ location.currency }}<br>
              <strong>Organization:</strong> {{ location.org }}<br>
              <strong>AS:</strong> {{ location.as }}<br>
              <strong>AS Name:</strong> {{ location.asname }}<br>
              <strong>Mobile:</strong> {{ location.mobile }}<br>
              <strong>Proxy:</strong> {{ location.proxy }}<br>
              <strong>Hosting:</strong> {{ location.hosting }}<br>
            </div>
          </li>
          {% endfor %}
        </ul>
      </div>
    </div>
    {% else %}
    <p class="text-info">No geolocation results found.</p>
    {% endif %}
  </div>

  <!-- Bootstrap JS and dependencies (not strictly necessary for appearance) -->
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
</body>
<div>

</div>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def ip_lookup():
    locations = None
    map_url = None
    top_5_ips = None
    if request.method == 'POST':
        ips_input = request.form['ipsInput']
        ips = ips_input.split()
        locations, top_5_ips = bulk_lookup(ips)
        if locations:
            map_url = generate_google_maps_url(locations)
    
    return render_template_string(html_template, locations=locations, map_url=map_url, top_5_ips=top_5_ips)

if __name__ == '__main__':
    app.run(debug=True)










# made by (CW165) Harjinder Singh
