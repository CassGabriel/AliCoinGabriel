import sys, json, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer, QDateTime
from PyQt5.QtNetwork import QNetworkCookie

class AliExpressCoinCollector(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AliExpress Coin Collector")
        self.setFixedSize(475, 812)
        self.cookies_file = "cookies.json"

        mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        self.page().profile().setHttpUserAgent(mobile_ua)

        self.page().loadFinished.connect(self.on_page_loaded)

        QTimer.singleShot(3000, lambda: self.load(QUrl("https://m.aliexpress.com/p/coin-index/index.html")))

    def on_page_loaded(self):
        self.save_cookies()
        if "coin-index" in self.url().toString():
            self.collect_coins()

    def save_cookies(self):
        store = self.page().profile().cookieStore()
        cookies_list = []

        def on_cookie_added(cookie):
            cookies_list.append({
                "name": bytes(cookie.name()).decode(),
                "value": bytes(cookie.value()).decode(),
                "domain": cookie.domain(),
                "path": cookie.path(),
                "secure": cookie.isSecure(),
                "httpOnly": cookie.isHttpOnly(),
                "expirationDate": cookie.expirationDate().toSecsSinceEpoch() if not cookie.isSessionCookie() else None
            })

        store.cookieAdded.connect(on_cookie_added)

        def write_cookies():
            with open(self.cookies_file, "w") as f:
                json.dump(cookies_list, f)
            print("Cookies salvos.")
            store.cookieAdded.disconnect(on_cookie_added)

        write_cookies()

    def collect_coins(self):
        script = """
            (async () => {
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }

                async function clickBySelector(selector) {
                    let el = document.querySelector(selector);
                    if (el) {
                        el.click();
                        await sleep(1000);
                        return true;
                    }
                    return false;
                }

                async function doTasks() {
                    let taskBtns = Array.from(document.querySelectorAll('div.e2e_normal_task_right_btn'));
                    for (let i = 0; i < taskBtns.length; i++) {
                        if (taskBtns[i] && (taskBtns[i].innerText.toLowerCase().includes("go") || taskBtns[i].innerText.toLowerCase().includes("ir"))) {
                            taskBtns[i].click();
                            await sleep(1000);
                        }
                    }
                }

                async function closeDrawer() {
                    await clickBySelector("div.aecoin-drawer-header-close-3pGfZ");
                    await sleep(1000);
                }

                let clickedMain = false;
                if (await clickBySelector(".aecoin-button-2KJzt.aecoin-unchecked-3rjes.aecoin-scaleIdle-2RACs")) {
                    clickedMain = true;
                }

                for (let i = 0; i < 3; i++) {
                    let elMainChecked = document.querySelector(".aecoin-button-2KJzt.aecoin-checked-3eXDN");
                    if (elMainChecked) {
                        elMainChecked.click();
                        await sleep(2000);
                        await doTasks();
                        await closeDrawer();
                        await sleep(2000);
                    }
                }

                return {clickedMain};
            })();
        """
        self.page().runJavaScript(script, lambda r: print(f"Ações realizadas: {r}"))
        QTimer.singleShot(10000, self.collect_coins)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    collector = AliExpressCoinCollector()
    collector.show()
    QTimer.singleShot(120000, app.quit)
    sys.exit(app.exec_())
