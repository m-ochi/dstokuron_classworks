#!/opt/homebrew/bin/python3
"""
食べログ「大分市 ラーメン」Seleniumクローラー
- 検索結果から全店舗URLを収集
- 各店舗の基本情報を取得
- 各店舗の口コミタブからレビューを収集
- tabelog_oita_ramen_stores.csv / tabelog_oita_ramen_reviews.csv に保存
"""

import time
import csv
import random
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ---- 設定 ---------------------------------------------------------------
SEARCH_KEYWORD  = "ラーメン"
SEARCH_AREA     = "大分市"
# 大分市のエリアコード（tabelog URL 用）
AREA_PATH       = "/oita/A4402/A440202"
BASE_URL        = "https://tabelog.com"
MAX_SEARCH_PAGES  = 3   # 検索結果の最大ページ数
MAX_REVIEW_PAGES  = 3   # 1店舗あたりの口コミ最大ページ数
OUTPUT_DIR      = Path(__file__).parent
STORES_CSV      = OUTPUT_DIR / "tabelog_oita_ramen_stores.csv"
REVIEWS_CSV     = OUTPUT_DIR / "tabelog_oita_ramen_reviews.csv"
HEADLESS        = False  # True にするとブラウザ非表示

WAIT_SHORT = (1.5, 3.0)   # ページ間の待機時間（秒）レンジ
WAIT_LONG  = (3.0, 5.0)
# -------------------------------------------------------------------------


def sleep(range_=WAIT_SHORT):
    time.sleep(random.uniform(*range_))


def setup_driver() -> webdriver.Chrome:
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    # ボット検出回避：WebDriver フラグを隠す
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=opts)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    return driver


# ---- ユーティリティ -------------------------------------------------------

def safe_text(driver_or_el, css: str) -> str:
    try:
        return driver_or_el.find_element(By.CSS_SELECTOR, css).text.strip()
    except NoSuchElementException:
        return ""


def safe_attr(driver_or_el, css: str, attr: str) -> str:
    try:
        return driver_or_el.find_element(By.CSS_SELECTOR, css).get_attribute(attr) or ""
    except NoSuchElementException:
        return ""


def wait_for(driver, css: str, timeout: int = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css))
    )


# ---- 1. 検索結果から店舗 URL を収集 ----------------------------------------

def collect_store_urls(driver, max_pages: int = MAX_SEARCH_PAGES) -> list[str]:
    """「大分市 ラーメン」の検索結果から店舗URLリストを返す"""
    search_url = (
        f"{BASE_URL}{AREA_PATH}/rstLst/"
        f"?vs=1&sa={SEARCH_AREA}&sk={SEARCH_KEYWORD}&lid=top_navi_suggest"
    )
    store_urls: list[str] = []

    for page in range(1, max_pages + 1):
        url = search_url if page == 1 else f"{search_url}&p={page}"
        print(f"  [検索] page {page}: {url}")
        driver.get(url)
        sleep(WAIT_LONG)

        # 店舗リンクを取得
        items = driver.find_elements(By.CSS_SELECTOR, "a.list-rst__rst-name-target")
        if not items:
            print("  → 店舗が見つかりません。ページ終了。")
            break

        for a in items:
            href = a.get_attribute("href")
            if href and href not in store_urls:
                store_urls.append(href)

        print(f"  → {len(items)}件追加 (累計 {len(store_urls)}件)")

        # 次ページボタン確認
        try:
            driver.find_element(By.CSS_SELECTOR, "a.c-pagination__arrow--next")
        except NoSuchElementException:
            print("  → 次ページなし。終了。")
            break

    return store_urls


# ---- 2. 店舗詳細情報を取得 --------------------------------------------------

def get_store_info(driver, store_url: str) -> dict:
    driver.get(store_url)
    sleep(WAIT_SHORT)

    info: dict = {"store_url": store_url}

    # 店舗 ID（URL から抽出）
    m = re.search(r"/(\d{8})/?$", store_url.rstrip("/"))
    info["store_id"] = m.group(1) if m else ""

    # 店名（複数セレクタを試行）
    for sel in [
        "h2.display-name span",
        "h1.rstdtl-hd-restaurant-name__name",
        "h1.display-name",
        "h2.display-name",
    ]:
        name = safe_text(driver, sel)
        if name:
            info["store_name"] = name
            break
    else:
        info["store_name"] = ""

    # 総合評価
    for sel in [
        "span.rdheader-rating__score-val-dtl",
        "b.c-rating__val--score",
        "span.c-rating-v2__val",
    ]:
        score = safe_text(driver, sel)
        if score:
            info["score"] = score
            break
    else:
        info["score"] = ""

    # 住所
    for sel in [
        "p.rstinfo-table__val--address",
        "td.rstinfo-table__val span",
        "address",
    ]:
        addr = safe_text(driver, sel)
        if addr:
            info["address"] = addr
            break
    else:
        info["address"] = ""

    # ジャンル
    info["genre"] = safe_text(driver, "span.linktree__parent-target-text") or \
                    safe_text(driver, "a.linktree__parent-target")

    # 営業時間・定休日
    info["open_hours"] = safe_text(driver, "p.rstinfo-table__val--hours") or \
                         safe_text(driver, "td.rstinfo-table__val--hours")
    info["holiday"]    = safe_text(driver, "p.rstinfo-table__val--holiday") or \
                         safe_text(driver, "td.rstinfo-table__val--holiday")

    # 予算
    info["budget_dinner"] = safe_text(driver, "span#js-rstdtl-budget-dinner") or \
                            safe_attr(driver, "span#js-rstdtl-budget-dinner", "data-budget-dinner")
    info["budget_lunch"]  = safe_text(driver, "span#js-rstdtl-budget-lunch") or \
                            safe_attr(driver, "span#js-rstdtl-budget-lunch", "data-budget-lunch")

    return info


# ---- 3. 口コミタブからレビューを収集 ----------------------------------------

def _parse_review_items(items, store_id: str, store_name: str) -> list[dict]:
    """review item 要素群からレビュー辞書リストを返す"""
    reviews = []
    for item in items:
        def t(css):
            return safe_text(item, css)
        def a(css, attr):
            return safe_attr(item, css, attr)

        reviewer_href = a("a.rvw-item__rvwr-name", "href")   # /rvwr/XXXXXXXXX/
        reviewer_name = t("a.rvw-item__rvwr-name span") or t("a.rvw-item__rvwr-name")
        rating        = t("b.c-rating__val") or t("div.rvw-item__rvw-info b")
        title         = t("p.rvw-item__title strong") or t("p.rvw-item__title")
        date          = t("span.rvw-item__date")

        # レビュー本文（div.rvw-comment > p の全テキストを結合）
        try:
            paras = item.find_elements(By.CSS_SELECTOR, "div.rvw-comment p, div.rvw-item__rvw-comment p")
            review_text = "\n".join(p.text.strip() for p in paras if p.text.strip())
        except Exception:
            review_text = ""

        # 訪問目的・用途など補足情報
        use_type = t("span.rvw-item__use-service")

        reviews.append({
            "store_id":      store_id,
            "store_name":    store_name,
            "reviewer_id":   reviewer_href,
            "reviewer_name": reviewer_name,
            "rating":        rating,
            "title":         title,
            "date":          date,
            "use_type":      use_type,
            "review":        review_text,
        })
    return reviews


def get_store_reviews(driver, store_url: str, store_id: str, store_name: str,
                      max_pages: int = MAX_REVIEW_PAGES) -> list[dict]:
    """口コミ一覧ページを巡回してレビューを収集する"""
    review_base = store_url.rstrip("/") + "/dtlrvwlst/"
    all_reviews: list[dict] = []

    for page in range(1, max_pages + 1):
        url = review_base if page == 1 else f"{review_base}?COND_SORT=1&p={page}"
        print(f"    [口コミ] page {page}: {url}")
        driver.get(url)
        sleep(WAIT_SHORT)

        items = driver.find_elements(By.CSS_SELECTOR, "div.rvw-item")
        if not items:
            break

        batch = _parse_review_items(items, store_id, store_name)
        all_reviews.extend(batch)
        print(f"    → {len(batch)}件取得 (累計 {len(all_reviews)}件)")

        # 次ページの確認
        try:
            driver.find_element(By.CSS_SELECTOR, "a.c-pagination__arrow--next")
        except NoSuchElementException:
            break

    return all_reviews


# ---- 4. CSV 保存 -----------------------------------------------------------

def save_csv(rows: list[dict], path: Path, label: str):
    if not rows:
        print(f"  [WARN] {label} のデータがありません。スキップ。")
        return
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  → {label} を {path} に保存しました ({len(rows)} 件)")


# ---- メイン ----------------------------------------------------------------

def main():
    driver = setup_driver()

    all_store_info: list[dict] = []
    all_reviews:    list[dict] = []

    try:
        print("=" * 60)
        print(f"食べログ「{SEARCH_AREA} {SEARCH_KEYWORD}」クローラー開始")
        print("=" * 60)

        # ① 店舗 URL の収集
        print("\n--- Step 1: 検索結果から店舗 URL を収集 ---")
        store_urls = collect_store_urls(driver, max_pages=MAX_SEARCH_PAGES)
        print(f"\n合計 {len(store_urls)} 件の店舗を取得しました\n")

        # ② 各店舗の情報とレビューを収集
        print("--- Step 2: 各店舗の情報・口コミを収集 ---")
        for i, store_url in enumerate(store_urls, 1):
            print(f"\n[{i}/{len(store_urls)}] {store_url}")

            # 店舗情報
            info = get_store_info(driver, store_url)
            all_store_info.append(info)
            print(f"  店名: {info.get('store_name')}  スコア: {info.get('score')}  住所: {info.get('address')}")

            # レビュー
            reviews = get_store_reviews(
                driver, store_url,
                store_id=info.get("store_id", ""),
                store_name=info.get("store_name", ""),
                max_pages=MAX_REVIEW_PAGES,
            )
            all_reviews.extend(reviews)
            sleep(WAIT_LONG)

    except KeyboardInterrupt:
        print("\n\n中断されました。途中結果を保存します。")

    finally:
        driver.quit()

    # ③ CSV 保存
    print("\n--- Step 3: CSV 保存 ---")
    save_csv(all_store_info, STORES_CSV,  "店舗情報")
    save_csv(all_reviews,    REVIEWS_CSV, "口コミ")

    print("\n完了しました。")


if __name__ == "__main__":
    main()
