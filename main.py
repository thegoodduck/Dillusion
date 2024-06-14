#!/usr/bin/python3
# Importing required libraries
import sys
import_sucessfull = True
try:
    from PyQt5.QtCore import *
except ImportError:
    import subprocess
    root = tk.Tk()
    root.title("Installing Dependencies")
    label = tk.Label(root, text="Installing Dependencies...")
    label.pack()
    root.update()
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "--break-system-packages"])
    import_sucessfull = False
try:
    from PyQt5.QtWidgets import *
except ImportError:
    import subprocess
    root = tk.Tk()
    root.title("Installing Dependencies")
    label = tk.Label(root, text="Installing Dependencies...")
    label.pack()
    root.update()
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "--break-system-packages"])
    import_sucessfull = False

try:
    from PyQt5.QtGui import *
except ImportError:
    import subprocess
    root = tk.Tk()
    root.title("Installing Dependencies")
    label = tk.Label(root, text="Installing Dependencies...")
    label.pack()
    root.update()
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "--break-system-packages"])
    import_sucessfull = False

try:
    from PyQt5.QtWebEngineWidgets import *
except ImportError:
    import subprocess
    root = tk.Tk()
    root.title("Installing Dependencies")
    label = tk.Label(root, text="Installing Dependencies...")
    label.pack()
    root.update()
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "--break-system-packages"])
    import_sucessfull = False
try:
    from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
except ImportError:
    import subprocess
    root = tk.Tk()
    root.title("Installing Dependencies")
    label = tk.Label(root, text="Installing Dependencies...")
    label.pack()
    root.update()
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "--break-system-packages"])
    import_sucessfull = False


try:
    from PyQt5.QtNetwork import QNetworkProxy
except ImportError:
    import subprocess
    root = tk.Tk()
    root.title("Installing Dependencies")
    label = tk.Label(root, text="Installing Dependencies...")
    label.pack()
    root.update()
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "--break-system-packages"])
    import_sucessfull = False

import sys
import requests
import socket
import json
import time
if import_sucessfull != True:
    print("[INFO] Dependencies successfully installed")
    # Reimport all dependencies
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtWebEngineWidgets import *
    from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
    from PyQt5.QtNetwork import QNetworkProxy
    print("[INFO] Reimporting dependencies")


# Load ad selectors from file
try:
    with open("ad_selectors.json", "r") as file:
        ad_selectors = json.load(file)
except:
    print("[WARN] Could not load ad selectors")
    ad_selectors = []
class LoadingProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(LoadingProgressBar, self).__init__(*args, **kwargs)
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #1E90FF; /* Blue color */
                width: 10px;
            }
        """)
        self.setMaximum(100)
        self.setValue(0)
        self.setFormat("%v%")  # Display the progress value
        self.setAlignment(Qt.AlignCenter)
    def set_download_speed(self, speed):
        self.setFormat(f"{self.value()}% - {speed} Mbps")

class Adblocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_blocked_domains()

    # Load blocked domains from file
    def load_blocked_domains(self):
        with open("blocked_domains.json", "r") as file:
            self.blocked_domains = json.load(file)

    # Intercept request and block ads
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        for domain in self.blocked_domains:
            if domain in url:
                info.block(True)
                print(f"[DEBUG] Blocked ad request: {url}")
                break

# Method to hide ad elements
def hide_ad_elements(self):
    js_function = """
        function hideAdElements(selectors) {
            selectors.forEach(function(selector) {
                var elements = document.querySelectorAll(selector);
                elements.forEach(function(element) {
                    element.style.display = 'none';
                });
            });
        }
        hideAdElements(%s);
    """ % json.dumps(ad_selectors)
    self.tabs.currentWidget().page().runJavaScript(js_function, lambda _: None)
    print("[DEBUG] Ad elements hidden")


# Load ad selectors from file

class Adblocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_blocked_domains()

    # Load blocked domains from file
    def load_blocked_domains(self):
        try:
            with open("blocked_domains.json", "r") as file:
                self.blocked_domains = json.load(file)
        except:
            print("[WARN] Could not load blocked domains")
            self.blocked_domains = []
    # Intercept request and block ads
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        for domain in self.blocked_domains:
            if domain in url:
                info.block(True)
                print(f"[DEBUG] Blocked ad request: {url}")
                break

# Method to hide ad elements
def hide_ad_elements(self):
    js_function = """
        function hideAdElements(selectors) {
            selectors.forEach(function(selector) {
                var elements = document.querySelectorAll(selector);
                elements.forEach(function(element) {
                    element.style.display = 'none';
                });
            });
        }
        hideAdElements(%s);
    """ % json.dumps(ad_selectors)
    self.tabs.currentWidget().page().runJavaScript(js_function, lambda _: None)
    print("[DEBUG] Ad elements hidden")

class LoadingProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(LoadingProgressBar, self).__init__(*args, **kwargs)
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #1E90FF;
                width: 10px;
            }
        """)
        self.setMaximum(100)
        self.setValue(0)
        self.setFormat("")
        self.setAlignment(Qt.AlignTop)

    def set_download_speed(self, speed):
        self.setFormat("")

# Main window
class MainWindow(QMainWindow):


    # Constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.adblocker = Adblocker()
        self.page = QWebEnginePage()
        self.page.profile().setRequestInterceptor(self.adblocker)
        print("[DEBUG] Initializing main window")

        # Set window properties
        self.setWindowTitle("Dillusion Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Creating a loading progress bar
        self.loading_progress_bar = LoadingProgressBar(self)
        self.layout.addWidget(self.loading_progress_bar)

        # Creating a tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.layout.addWidget(self.tabs)

        # Creating a status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Creating a tool bar for navigation
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(24, 24))  # Set icon size for a modern look
        self.addToolBar(Qt.TopToolBarArea, navtb)

        # Creating navigation buttons with emojis
        back_btn = QAction("⬅️", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction("➡️", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction("🔄", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.setMaximumHeight(30)  # Set height for the URL bar
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("🛑", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        self.privacy_btn = QAction("🕵️", self)
        self.privacy_btn.setCheckable(True)
        self.privacy_btn.setStatusTip("Toggle Privacy Mode")
        self.privacy_btn.triggered.connect(self.toggle_privacy_mode)
        navtb.addAction(self.privacy_btn)

        self.tor_btn = QAction("🧅", self)
        self.tor_btn.setCheckable(True)
        self.tor_btn.setStatusTip("Toggle Tor Mode")
        self.tor_btn.triggered.connect(self.toggle_tor_mode)
        navtb.addAction(self.tor_btn)

        clear_cookies_btn = QAction("🧹", self)
        clear_cookies_btn.setStatusTip("Clear all cookies")
        clear_cookies_btn.triggered.connect(self.clear_cookies)
        navtb.addAction(clear_cookies_btn)

        new_tab_btn = QAction("🆕", self)
        new_tab_btn.setStatusTip('Open a new tab')
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl('http://www.google.com'), 'New Tab'))
        navtb.addAction(new_tab_btn)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.is_privacy_mode = False
        self.is_tor_mode = False
        self.tor_profile = None

        # Apply custom stylesheet
        self.apply_styles()

        # Show the window
        self.show()

    # Method for adding new tab
    def add_new_tab(self, qurl=None, label="Blank", profile=None):
        if qurl is None:
            qurl = QUrl('http://www.google.com')

        if profile is None:
            profile = QWebEngineProfile.defaultProfile()

        browser = QWebEngineView()
        page = QWebEnginePage(profile, browser)
        browser.setPage(page)
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))
        browser.loadFinished.connect(lambda: hide_ad_elements(self))
        browser.loadProgress.connect(self.update_loading_progress)
        browser.loadFinished.connect(lambda: self.loading_progress_bar.setValue(0))

        print(f"[DEBUG] New tab added with URL: {qurl.toString()}")

    # When double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
        if i == -1:
            print("[DEBUG] Double-click detected on tab bar, opening new tab")
            self.add_new_tab(QUrl('http://www.google.com'), 'New Tab')

    # When tab is changed
    def current_tab_changed(self, i):
        if self.tabs.count() == 0:
            return
        current_widget = self.tabs.currentWidget()
        if current_widget is None:
            return
        qurl = current_widget.url()
        self.update_urlbar(qurl, current_widget)
        self.update_title(current_widget)

        print(f"[DEBUG] Tab changed to index: {i}, URL: {qurl.toString()}")

    # When tab is closed
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        browser = self.tabs.widget(i)
        browser.deleteLater()
        self.tabs.removeTab(i)

        print(f"[DEBUG] Tab closed at index: {i}")

    # Method for updating the title
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Dillusion Browser" % title)

        print(f"[DEBUG] Window title updated: {title}")

    # Action to go to home
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
        print("[DEBUG] Navigating to home")

    # Method for navigate to URL
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        print(f"[DEBUG] Navigating to URL: {q.toString()}")
        self.perform_dns_spoof_check(q)

    # Method to update the URL bar
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

        print(f"[DEBUG] URL bar updated: {q.toString()}")

    # Method to toggle privacy mode
    def toggle_privacy_mode(self):
        urls = [self.tabs.widget(i).url() for i in range(self.tabs.count())]
        if self.is_privacy_mode:
            self.is_privacy_mode = False
            self.privacy_btn.setChecked(False)
            self.reload_tabs_with_profile(QWebEngineProfile.defaultProfile(), urls)
            print("[DEBUG] Privacy mode disabled")
        else:
            privacy_profile = QWebEngineProfile(self)
            privacy_profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
            privacy_profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
            self.is_privacy_mode = True
            self.privacy_btn.setChecked(True)
            self.reload_tabs_with_profile(privacy_profile, urls)
            print("[DEBUG] Privacy mode enabled")

    # Method to toggle Tor mode
    def toggle_tor_mode(self):
        urls = [self.tabs.widget(i).url() for i in range(self.tabs.count())]
        if self.is_tor_mode:
            self.is_tor_mode = False
            self.tor_btn.setChecked(False)
            QNetworkProxy.setApplicationProxy(QNetworkProxy())  # Reset to no proxy
            self.reload_tabs_with_profile(QWebEngineProfile.defaultProfile(), urls)
            print("[DEBUG] Tor mode disabled")
        else:
            self.tor_profile = QWebEngineProfile(self)
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.Socks5Proxy)
            proxy.setHostName("127.0.0.1")
            proxy.setPort(9050)
            QNetworkProxy.setApplicationProxy(proxy)
            self.is_tor_mode = True
            self.tor_btn.setChecked(True)
            self.reload_tabs_with_profile(self.tor_profile, urls)
            print("[DEBUG] Tor mode enabled")

    # Method to clear cookies
    def clear_cookies(self):
        profile = self.tabs.currentWidget().page().profile()
        profile.clearHttpCache()
        profile.cookieStore().deleteAllCookies()
        print("[DEBUG] Cookies cleared")

    # Method to reload all tabs with a given profile
    def reload_tabs_with_profile(self, profile, urls):
        self.tabs.clear()
        for url in urls:
            self.add_new_tab(url, profile=profile)
        print("[DEBUG] Tabs reloaded with new profile")

    # Method for DNS spoof check
    def perform_dns_spoof_check(self, qurl):
        domain = qurl.host()
        try:
            public_ip = socket.gethostbyname(domain)
            local_ip = socket.gethostbyname(domain)  # Use a local DNS resolver
            if public_ip == local_ip:
                print(f"[DEBUG] Public and local DNS match for {domain}, fetching directly")
                self.tabs.currentWidget().setUrl(qurl)
            else:
                print(f"[WARN] DNS mismatch for {domain}. Public IP: {public_ip}, Local IP: {local_ip}")
                self.tabs.currentWidget().setUrl(QUrl(f"http://{public_ip}"))
        except socket.gaierror as e:
            print(f"[FATAL] DNS resolution failed for {domain}: {e}")
            if "chrome://" in qurl.toString():
                self.tabs.currentWidget().setUrl(qurl)
            QMessageBox.critical(self, 'DNS Error', f"Failed to resolve DNS for {domain}: {e}")
            try:
                self.tabs.currentWidget().setUrl(qurl)
            except socket.herror as e:
                QMessageBox.critical(self, 'Fatal', f"{domain} crashed the browser {e}")

    # Method to update the loading progress
    def update_loading_progress(self, value):
        self.loading_progress_bar.setValue(value)
        if value == 100:
            download_speed = self.get_download_speed()
            self.loading_progress_bar.set_download_speed("")

    # Method to get the download speed
    def get_download_speed(self):
        page = self.tabs.currentWidget().page()
        start_time = time.time()
        total_bytes = 0

        def callback(bytes_received):
            nonlocal total_bytes
            total_bytes += bytes_received

        page.loadProgress.connect(callback)
        time.sleep(1)
        elapsed_time = time.time() - start_time
        download_speed = (total_bytes / elapsed_time) / (1024 * 1024)
        return ""

    # Apply custom stylesheet
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QToolBar {
                background: #FFFFFF;
                padding: 5px;
                border: none;
            }
            QTabWidget::pane {
                border-top: 2px solid #C2C7CB;
                position: absolute;
                top: -0.5em;
                background: #FFFFFF;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #E0E0E0;
                border: 1px solid #C4C4C3;
                padding: 10px;
                border-radius: 5px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #FFFFFF;
            }
            QLineEdit {
                border: 1px solid #C4C4C3;
                border-radius: 5px;
                padding: 5px;
            }
            QStatusBar {
                background: #FFFFFF;
                padding: 3px;
            }
            QToolButton {
                border: none;
                background: transparent;
            }
            QToolButton:hover {
                background: #E0E0E0;
                border-radius: 5px;
            }
        """)
        print("[DEBUG] Styles applied")


# Creating a PyQt5 application
app = QApplication(sys.argv)
app.setApplicationName("Dillusion Browser")

# Creating MainWindow object
window = MainWindow()
app.exec_()