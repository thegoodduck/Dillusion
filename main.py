#!/usr/bin/python3
# Importing required libraries
import sys
import tkinter as tk
import subprocess
import json
import time
import requests
import socket
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtNetwork import QNetworkProxy

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
        self.blocked_ad_count = 0

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
                self.blocked_ad_count += 1
                print(f"[DEBUG] Blocked ad request: {url}")
                break

    def get_blocked_ad_count(self):
        return self.blocked_ad_count

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

        ad_count_btn = QAction("📊", self)
        ad_count_btn.setStatusTip('Show blocked ad count')
        ad_count_btn.triggered.connect(self.show_blocked_ad_count)
        navtb.addAction(ad_count_btn)

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

    # Close current tab
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)
        print(f"[DEBUG] Tab closed at index: {i}")

    # Update window title
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Dillusion Browser")

    # Navigate to home page
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
        print("[DEBUG] Navigating to homepage")

    # Navigate to URL
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)
        print(f"[DEBUG] Navigating to URL: {q.toString()}")

    # Update URL bar
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        print(f"[DEBUG] URL bar updated to: {q.toString()}")

    # Clear cookies
    def clear_cookies(self):
        profile = self.tabs.currentWidget().page().profile()
        profile.clearAllVisitedLinks()
        profile.cookieStore().deleteAllCookies()
        print("[DEBUG] Cookies cleared")

    # Apply custom styles
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QToolBar {
                background-color: #E9E9ED;
                border: none;
                padding: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #C1C1C1;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                border: 1px solid #C1C1C1;
                border-bottom: none;
            }
            QTabBar::tab {
                background-color: #F9F9FA;
                border: 1px solid #C1C1C1;
                padding: 5px 10px;
                margin-right: 2px;
            }
            QLineEdit {
                padding: 3px;
                border: 1px solid #C1C1C1;
                border-radius: 2px;
                font-size: 14px;
            }
            QProgressBar {
                border: 1px solid #C1C1C1;
                border-radius: 2px;
                background-color: #FFFFFF;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0A84FF;
                width: 10px;
            }
        """)
        print("[DEBUG] Firefox-like styles applied")


    # Toggle privacy mode
    def toggle_privacy_mode(self):
        self.is_privacy_mode = not self.is_privacy_mode
        if self.is_privacy_mode:
            print("[DEBUG] Privacy mode enabled")
            # Enable privacy features here
        else:
            print("[DEBUG] Privacy mode disabled")
            # Disable privacy features here

    # Toggle Tor mode
    def toggle_tor_mode(self):
        self.is_tor_mode = not self.is_tor_mode
        if self.is_tor_mode:
            print("[DEBUG] Tor mode enabled")
            self.tor_profile = QWebEngineProfile("tor_profile", self)
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.Socks5Proxy)
            proxy.setHostName("localhost")
            proxy.setPort(9050)
            self.tor_profile.setRequestInterceptor(self.adblocker)
            self.add_new_tab(profile=self.tor_profile)
        else:
            print("[DEBUG] Tor mode disabled")
            self.tor_profile = None
            self.add_new_tab()

    # Show blocked ad count
    def show_blocked_ad_count(self):
        count = self.adblocker.get_blocked_ad_count()
        QMessageBox.information(self, "Blocked Ads", f"Blocked Ad Requests: {count}")
        print(f"[DEBUG] Blocked ad count shown: {count}")

    # Update loading progress
    def update_loading_progress(self, progress):
        self.loading_progress_bar.setValue(progress)
        print(f"[DEBUG] Loading progress: {progress}%")

    # Detect if the connection is HTTPS
    def is_https(self, url):
        return url.scheme() == 'https'

    def add_secure_button(self):
        secure_btn = QAction("🔒", self)
        secure_btn.setCheckable(True)
        secure_btn.setChecked(self.is_https(self.tabs.currentWidget().url()))
        secure_btn.setStatusTip("Toggle Secure Mode")
        secure_btn.triggered.connect(self.toggle_secure_mode)
        navtb.addAction(secure_btn)

    def toggle_secure_mode(self, checked):
        if checked:
            self.tabs.currentWidget().setUrl(QUrl(f"https://{self.tabs.currentWidget().url().host()}"))
        else:
            self.tabs.currentWidget().setUrl(QUrl(f"http://{self.tabs.currentWidget().url().host()}"))
    # Enable file downloads
    def enable_file_downloads(self):
        self.page.profile().setHttpAcceptRequestHeaders(['application/octet-stream'])
        self.page.profile().setHttpAcceptResponseHeaders(['application/octet-stream'])
        self.page.downloadRequested.connect(self.download_file)
        print("[DEBUG] File downloads enabled")

    def download_file(self, download):
        download.accept()
        print(f"[DEBUG] Downloading file: {download.url().toString()}")

# Main entry point
app = QApplication(sys.argv)
QApplication.setApplicationName("Dillusion Browser")
main_window = MainWindow()
app.exec_()
