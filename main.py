import requests
from flask import Flask, request, render_template
from fake_useragent import UserAgent

app = Flask(__name__)

# Global variable for proxy configuration
proxy_mode = 'direct'  # Default mode is direct connection
proxies = None

# Function to switch proxy mode
def switch_proxy_mode(mode):
    global proxy_mode, proxies
    proxy_mode = mode
    if mode == 'tor':
        proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050',
        }
    else:
        proxies = None

# Function to fetch web page content
def fetch_content(url):
    if proxies:
        response = requests.get(url, proxies=proxies)
    else:
        response = requests.get(url)
    return response.text

# Function to test for censorship
def test_censorship(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    global proxy_mode
    if request.method == 'POST':
        url = request.form['url']
        proxy_mode = request.form.get('proxy_mode', 'direct')
        switch_proxy_mode(proxy_mode)
        content = fetch_content(url)
        censorship_test_result = test_censorship(url)
        return render_template('index.html', url=url, content=content, censorship_test_result=censorship_test_result, proxy_mode=proxy_mode)
    return render_template('index.html', proxy_mode=proxy_mode)

if __name__ == '__main__':
    app.run(debug=True)
