# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtNetwork import QNetworkProxy
import sys
import requests

# main window
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a tab widget
        self.tabs = QTabWidget()

        # making document mode true
        self.tabs.setDocumentMode(True)

        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # making tabs closeable
        self.tabs.setTabsClosable(True)

        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # making tabs as central widget
        self.setCentralWidget(self.tabs)

        # creating a status bar
        self.status = QStatusBar()

        # setting status bar to the main window
        self.setStatusBar(self.status)

        # creating a tool bar for navigation
        navtb = QToolBar("Navigation")

        # adding tool bar to the main window
        self.addToolBar(navtb)

        # creating back action
        back_btn = QToolButton()
        back_btn.setText("🔙")
        back_btn.setToolTip("Back")
        back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        navtb.addWidget(back_btn)

        # similarly adding next button
        next_btn = QToolButton()
        next_btn.setText("🔜")
        next_btn.setToolTip("Forward")
        next_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addWidget(next_btn)

        # similarly adding reload button
        reload_btn = QToolButton()
        reload_btn.setText("🔄")
        reload_btn.setToolTip("Reload")
        reload_btn.clicked.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addWidget(reload_btn)

        # creating home action
        home_btn = QToolButton()
        home_btn.setText("🏠")
        home_btn.setToolTip("Home")
        home_btn.clicked.connect(self.navigate_home)
        navtb.addWidget(home_btn)

        # adding a separator
        navtb.addSeparator()

        # creating a line edit widget for URL
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        # similarly adding stop action
        stop_btn = QToolButton()
        stop_btn.setText("⏹️")
        stop_btn.setToolTip("Stop")
        stop_btn.clicked.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addWidget(stop_btn)

        # creating privacy mode action
        self.privacy_btn = QToolButton()
        self.privacy_btn.setText("🕵️‍♂️")
        self.privacy_btn.setToolTip("Toggle Privacy Mode")
        self.privacy_btn.setCheckable(True)
        self.privacy_btn.clicked.connect(self.toggle_privacy_mode)
        navtb.addWidget(self.privacy_btn)

        # creating Tor mode action
        self.tor_btn = QToolButton()
        self.tor_btn.setText("🕸️")
        self.tor_btn.setToolTip("Toggle Tor Mode")
        self.tor_btn.setCheckable(True)
        self.tor_btn.clicked.connect(self.toggle_tor_mode)
        navtb.addWidget(self.tor_btn)

        # creating clear cookies action
        clear_cookies_btn = QToolButton()
        clear_cookies_btn.setText("🍪🚫")
        clear_cookies_btn.setToolTip("Clear all cookies")
        clear_cookies_btn.clicked.connect(self.clear_cookies)
        navtb.addWidget(clear_cookies_btn)

        # creating new tab button
        new_tab_btn = QToolButton()
        new_tab_btn.setText("➕")
        new_tab_btn.setToolTip('New Tab')
        new_tab_btn.clicked.connect(lambda: self.add_new_tab(QUrl('http://www.google.com'), 'New Tab'))
        navtb.addWidget(new_tab_btn)

        # adding action for manually adding bridges
        manual_bridges_btn = QToolButton()
        manual_bridges_btn.setText("➕🕸️")
        manual_bridges_btn.setToolTip('Add Bridges Manually')
        manual_bridges_btn.clicked.connect(self.add_manual_bridges)
        navtb.addWidget(manual_bridges_btn)

        # adding action for automatically fetching bridges
        auto_bridges_btn = QToolButton()
        auto_bridges_btn.setText("🔍🕸️")
        auto_bridges_btn.setToolTip('Fetch Bridges Automatically')
        auto_bridges_btn.clicked.connect(self.fetch_bridges_automatically)
        navtb.addWidget(auto_bridges_btn)

        # creating first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        # showing all the components
        self.show()

        # setting window title
        self.setWindowTitle("Dillusion Browser")

        # Variables to track current modes
        self.is_privacy_mode = False
        self.is_tor_mode = False
        self.tor_profile = None

    # method for adding new tab
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

    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab(QUrl('http://www.google.com'), 'New Tab')

    # when tab is changed
    def current_tab_changed(self, i):
        if self.tabs.count() == 0:
            return
        current_widget = self.tabs.currentWidget()
        if current_widget is None:
            return
        qurl = current_widget.url()
        self.update_urlbar(qurl, current_widget)
        self.update_title(current_widget)

    # when tab is closed
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        browser = self.tabs.widget(i)
        browser.deleteLater()  # Properly delete the widget
        self.tabs.removeTab(i)

    # method for updating the title
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Dillusion Browser" % title)

    # action to go to home
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    # method for navigate to url
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    # method to update the url
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # method to toggle privacy mode
    def toggle_privacy_mode(self):
        urls = [self.tabs.widget(i).url() for i in range(self.tabs.count())]
        if self.is_privacy_mode:
            self.is_privacy_mode = False
            self.privacy_btn.setChecked(False)
            self.reload_tabs_with_profile(QWebEngineProfile.defaultProfile(), urls)
        else:
            privacy_profile = QWebEngineProfile(self)
            privacy_profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
            privacy_profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
            self.is_privacy_mode = True
            self.privacy_btn.setChecked(True)
            self.reload_tabs_with_profile(privacy_profile, urls)

    # method to toggle Tor mode
    def toggle_tor_mode(self):
        urls = [self.tabs.widget(i).url() for i in range(self.tabs.count())]
        if self.is_tor_mode:
            self.is_tor_mode = False
            self.tor_btn.setChecked(False)
            QNetworkProxy.setApplicationProxy(QNetworkProxy())  # Reset to no proxy
            self.reload_tabs_with_profile(QWebEngineProfile.defaultProfile(), urls)
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

    # method to clear cookies
    def clear_cookies(self):
        profile = self.tabs.currentWidget().page().profile()
        profile.clearHttpCache()
        profile.cookieStore().deleteAllCookies()

    # method to reload all tabs with a given profile
    def reload_tabs_with_profile(self, profile, urls):
        self.tabs.clear()
        for url in urls:
            self.add_new_tab(url, profile=profile)

    # method to manually add bridges
    def add_manual_bridges(self):
        text, ok = QInputDialog.getText(self, 'Manual Bridges', 'Enter Bridges (comma separated):')
        if ok and text:
            bridges = [bridge.strip() for bridge in text.split(',')]
            self.configure_tor_with_bridges(bridges)

    # method to fetch bridges automatically
    def fetch_bridges_automatically(self):
        url = "https://bridges.torproject.org/bridges?transport=obfs4"
        headers = {
            "User-Agent": "Tor Browser",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                bridges = response.text.strip().split('\n')
                self.configure_tor_with_bridges(bridges)
            else:
                QMessageBox.critical(self, 'Error', f"Failed to fetch bridges: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, 'Error', f"Failed to fetch bridges: {e}")

    # method to configure Tor with bridges

    def configure_tor_with_bridges(self, bridges):
            if not self.is_tor_mode:
                QMessageBox.warning(self, 'Warning', 'Tor mode is not enabled.')
                return
            if not self.tor_profile:
                QMessageBox.warning(self, 'Warning', 'Tor profile is not initialized.')
                return
            for bridge in bridges:
                try:
                    self.tor_profile.setRequestInterceptor(QtWebEngine.QWebEngineUrlRequestInfo.ResourceTypeOther, bridge)
                except:
                    QMessageBox.warning(self, 'Error', 'Failed to add bridge. Please note the feature is experimental.')
                    return

# creating a PyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Dillusion Browser") 

# creating MainWindow object
window = MainWindow()

# loop
app.exec_()
