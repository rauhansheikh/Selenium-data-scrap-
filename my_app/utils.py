from .models import SearchResult

def scrape_google_results(query):
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import undetected_chromedriver as uc
    import types

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)

    uc.Chrome.__del__ = lambda self: None
    driver.set_page_load_timeout(30)
    driver.get("https://www.google.com/")

    try:
        try:
            time.sleep(2)
            consent_button = driver.find_element(By.XPATH, "//button[.//div[text()='I agree']]")
            consent_button.click()
            time.sleep(2)
        except:
            pass

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        all_results = []
        for _ in range(2):  # scrape 2 pages
            results = driver.find_elements(By.CSS_SELECTOR, 'div#search .tF2Cxc')
            for result in results:
                try:
                    title = result.find_element(By.TAG_NAME, "h3").text
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    try:
                        snippet = result.find_element(By.CSS_SELECTOR, ".VwiC3b").text
                    except:
                        snippet = ""

                    all_results.append((title, link, snippet))  # ✅ 3 values

                    # Optional: Save to DB
                    SearchResult.objects.create(query=query, title=title, link=link)

                except:
                    continue

            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_button.click()
                time.sleep(2)
            except:
                break

    finally:
        try:
            driver.quit()
        except:
            pass

    return all_results
