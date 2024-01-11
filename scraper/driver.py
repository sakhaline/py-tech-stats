from selenium import webdriver


class ChromeDriver:
    _instance = None

    def __new__(cls) -> "ChromeDriver":
        if not cls._instance:
            cls._instance = super(ChromeDriver, cls).__new__(cls)
            cls._instance.web_driver = webdriver.Chrome()
        return cls._instance

    def __enter__(self) -> "ChromeDriver":
        return self._instance.web_driver

    def __exit__(self,
                 exc_type: type,
                 exc_val: Exception,
                 exc_tb: type) -> None:
        self._instance.web_driver.close()
