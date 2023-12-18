import time
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger
from os import makedirs, path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

base_dir = path.dirname(path.abspath(__file__))
subj_dir = path.join(base_dir, "subjects")
makedirs(base_dir, exist_ok=True)
makedirs(subj_dir, exist_ok=True)

logger = getLogger(__name__)
handler_s = StreamHandler()
handler_f = FileHandler(path.join(base_dir, "scraping.log"), encoding="utf-8")
handler_s.setLevel(DEBUG)
handler_f.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler_s)
logger.addHandler(handler_f)
fmt = Formatter("%(asctime)s %(funcName)s %(message)s")
handler_s.setFormatter(fmt)
handler_f.setFormatter(fmt)


def main():
    syllabus = "https://benten.meisei-u.ac.jp/uprx/up/pk/pky001/Pky00101.xhtml?guestlogin=Kmh006"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(syllabus)

    loading_wait(driver)
    set_term(driver)
    with open(
        path.join(
            base_dir,
            "error.log",
        ),
        "w",
        encoding="utf-8",
    ) as err_f:
        for yobi in range(1, 7):
            click_yobi(driver, yobi)
            for jigen in range(1, 7):
                click_jigen(driver, jigen)

                # 検索
                loading_wait(driver)
                serach(driver)

                loading_wait(driver)
                for subj_n in range(get_subj_num(driver)):
                    logger.info(f"sta : {yobi}-{jigen}-{subj_n:03}")
                    try:
                        time.sleep(1)

                        loading_wait(driver)
                        open_subj(driver, subj_n)

                        loading_wait(driver)
                        save_subj(driver, yobi, jigen, subj_n)

                        loading_wait(driver)
                        close_subj(driver)
                    except Exception:
                        err_f.write(f"{yobi} {jigen} {subj_n}\n")
                        try:
                            loading_wait(driver)
                            close_subj(driver)
                        except Exception:
                            pass
                    loading_wait(driver)
                    logger.info(f"fin : {yobi}-{jigen}-{subj_n:03}")

                # チェックを外す
                click_jigen(driver, jigen)
            click_yobi(driver, yobi)

    driver.quit()


def serach(driver):
    try:
        # loading_wait(driver)
        driver.find_element(By.CSS_SELECTOR, "#funcForm\:search > span").click()
        # loading_wait(driver)
    except Exception as e:
        logger.info(e)
        raise


# 対象学期を全てに変更
def set_term(driver):
    try:
        # プルダウンをクリック
        driver.find_element(
            By.CSS_SELECTOR,
            "#funcForm\:kaikoGakki > div.ui-selectonemenu-trigger.ui-state-default.ui-corner-right > span",
        ).click()
        # 全て対象をクリック
        driver.find_element(
            By.CSS_SELECTOR,
            "#funcForm\:kaikoGakki_panel > div > ul > li:nth-child(1)",
        ).click()
    except Exception as e:
        logger.info(e)
        raise


def click_yobi(driver, yobi: int = 1):
    try:
        driver.find_element(
            By.CSS_SELECTOR, f"#funcForm\:yobiList > tbody > tr > td:nth-child({yobi*2}) > label"
        ).click()
    except Exception as e:
        logger.info(e)
        raise


def click_jigen(driver, jigen: int = 1):
    try:
        driver.find_element(
            By.CSS_SELECTOR, f"#funcForm\:jigenList > tbody > tr > td:nth-child({jigen*2}) > label"
        ).click()
    except Exception as e:
        logger.info(e)
        raise


def open_subj(driver, n: int = 0):
    try:
        # loading_wait(driver)
        driver.find_element(By.CSS_SELECTOR, f"#funcForm\:table\:{n}\:jugyoKmkName").click()
        # loading_wait(driver)
    except Exception as e:
        logger.info(e)
        raise


def close_subj(driver):
    try:
        # loading_wait(driver)
        driver.find_element(
            By.CSS_SELECTOR,
            "#pkx02301\:dialog > div.ui-dialog-titlebar.ui-widget-header.ui-helper-clearfix.ui-corner-top.ui-draggable-handle > a.ui-dialog-titlebar-icon.ui-dialog-titlebar-close.ui-corner-all > span",
        ).click()
        # loading_wait(driver)
    except Exception as e:
        logger.info(e)
        raise


def get_subj_num(driver):
    try:
        loading_wait(driver)
        elm = driver.find_element(
            By.CSS_SELECTOR,
            "#funcForm\:table_paginator_bottom > span.ui-paginator-current",
        )
        # loading_wait(driver)
        # print(elm.text.split("件"))
        return int(elm.text.split("件")[0])
    except Exception as e:
        logger.info(e)
        raise


def save_subj(driver, yobi, jigen, subj_n):
    try:
        # loading_wait(driver)
        source = driver.find_element(By.CSS_SELECTOR, "#pkx02301\:ch\:table").get_attribute(
            "innerHTML"
        )
        with open(
            path.join(
                subj_dir,
                f"{yobi}-{jigen}-{subj_n:03}.html",
            ),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(source)
        # loading_wait(driver)
    except Exception as e:
        logger.info(e)
        raise


def loading_wait(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "#j_idt39")))


if __name__ == "__main__":
    main()
