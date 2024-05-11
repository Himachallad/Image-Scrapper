from playwright.sync_api import sync_playwright
from time import sleep
import requests
import re
import os

try:
    os.system("pip install --quiet -r requirements.txt")
    os.system("playwright install chrome")
except:
    pass

pattern = r'^https://.*'

def create_folder_if_not_exists(folder_name):
    try:
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    except Exception as e:
        pass



create_folder_if_not_exists("output")

def download_image(image_url, img_name, search):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9"
            }

    img_data = requests.get(url=image_url, headers=headers).content
    
    image_dir = os.path.join(os.getcwd(), "output")
    image_dir = os.path.join(image_dir, search)
    create_folder_if_not_exists(image_dir)


    with open(os.path.join(image_dir, ("_").join(img_name.split(" ")) + '.png'), 'wb') as handler:
        handler.write(img_data)


def scrap_images(search, headless):
    print("Output will be stored in images directory")
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    page = browser.new_page()
    

    page.goto("https://images.google.com/")
    page.fill('textarea[role="combobox"]', value=search)
    page.keyboard.press("Enter")
    sleep(2)
    images = page.locator('//a//img[@width > 200]')
    
    for image in images.all():
        image.click()
        sleep(2)
        alt_text  = image.get_attribute('alt')

        found_images = page.get_by_alt_text(alt_text).all()

        for img in found_images:
            if re.match(pattern, img.get_attribute('src')):
                download_image(img.get_attribute('src'), alt_text, search)
    
    sleep(2)

def custom_input(prompt, default=None) -> str:
        if default is not None:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            return user_input if user_input else default
        else:
            return input(prompt)

try:        
    scrap_images(custom_input("Enter a keyword for which you want images", "Robot"), False)
except Exception as e:
    pass