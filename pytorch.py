import asyncio
from playwright.async_api import async_playwright
import pandas as pd


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        main_page = await browser.new_page()
        base_url = "https://discuss.pytorch.org"
        try:
            print("Navigating to the main page...")
            await main_page.goto(f"{base_url}//latest", timeout=60000)
            await main_page.wait_for_load_state("domcontentloaded")
            print("Main page loaded.")
        except Exception as e:
            print(f"Failed to load {base_url}//latest: {e}")
            await browser.close()
            return

        posts_data = []
        visited_urls = set()

        while True:
            print("Fetching posts...")
            posts_elements = await main_page.query_selector_all(
                "xpath=//a[contains(@class, 'title raw-link raw-topic-link')]"
            )

            new_posts = False
            for post_element in posts_elements:
                post_url = await post_element.get_attribute("href")
                if post_url is None:
                    continue

                full_post_url = f"{base_url}{post_url}"

                if full_post_url in visited_urls:
                    continue

                new_posts = True
                visited_urls.add(full_post_url)
                print(f"Processing post: {full_post_url}")

                # Open post in a new page (tab)
                post_page = await browser.new_page()
                try:
                    await post_page.goto(full_post_url)
                    await post_page.wait_for_load_state("domcontentloaded")

                    post_title_element = await post_page.query_selector(
                        "xpath=//a[@class='title raw-link raw-topic-link']"
                    )
                    post_title = (
                        await post_title_element.text_content()
                        if post_title_element
                        else "N/A"
                    )

                    category_name_element = await post_page.query_selector(
                        "xpath=//a[contains(@class, 'discourse-tag box')]"
                    )
                    category_name = (
                        await category_name_element.text_content()
                        if category_name_element
                        else "N/A"
                    )

                    tags_elements = await post_page.query_selector_all(
                        "xpath=//div[contains(@class, 'discourse-tags')]/a"
                    )
                    tags_text = ", ".join(
                        [await tag.text_content() for tag in tags_elements]
                    )

                    timestamp_element = await post_page.query_selector(
                        "xpath=//span[contains(@class, 'relative-date')]"
                    )
                    timestamp = (
                        await timestamp_element.get_attribute("data-time")
                        if timestamp_element
                        else "N/A"
                    )

                    username_element = await post_page.query_selector(
                        "xpath=(//span[contains(@class, 'username')]/a)[1]"
                    )
                    username = (
                        await username_element.text_content()
                        if username_element
                        else "N/A"
                    )

                    post_text_element = await post_page.query_selector(
                        "xpath=(//div[contains(@class, 'cooked')])[1]"
                    )
                    post_text = (
                        await post_text_element.inner_html()
                        if post_text_element
                        else "N/A"
                    )

                    posts_data.append(
                        {
                            "post_title": post_title.strip(),
                            "post_URL": full_post_url.strip(),
                            "category_name": category_name.strip(),
                            "tags": tags_text.strip(),
                            "timestamp": timestamp,
                            "username": username.strip(),
                            "post_text": post_text.strip(),
                        }
                    )

                except Exception as e:
                    print(f"An error occurred while processing {full_post_url}: {e}")
                finally:
                    await post_page.close()

            if not new_posts:
                print("No new posts found, ending scraping.")
                break

            print("Scrolling down...")
            await main_page.mouse.wheel(0, 15000)
            await asyncio.sleep(3)

        print("Saving data and closing browser...")
        timestamp_str = pd.Timestamp("now").strftime("%Y%m%d_%H%M%S")
        filename = f"posts_info_{timestamp_str}.csv"
        posts_df = pd.DataFrame(posts_data)
        posts_df.to_csv(filename, index=False)
        await browser.close()


asyncio.run(main())
