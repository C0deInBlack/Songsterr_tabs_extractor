#!/usr/bin/python3

import asyncio, sys, json, os, subprocess
from time import sleep
#sys.path.append('libs/lib/python3.13/site-packages')
from playwright.async_api import async_playwright
from rich.console import Console 
from rich.progress import Progress

async def get_tabs_urls(tmp_email: str, songs_urls: list[str], path: str) -> None:
    urls: list[str] = []
    async with async_playwright() as p:
        # browser = await p.firefox.launch(headless=False, slow_mo=50)
        browser = await p.firefox.launch()
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto('https://www.songsterr.com/a/wa/signup')

        await page.fill('div.io1ov:nth-child(2) > input:nth-child(1)', 'test') # Send username
        await page.fill('div.io1ov:nth-child(3) > input:nth-child(1)', tmp_email) # Send temp email
        await page.fill('div.io1ov:nth-child(4) > input:nth-child(1)', 'my_passwd') # Sen password

        await page.click('.Bd2y0') # Cick in 'agree with terms'
        await page.click('#signup') # Click in 'Create account'

        # await page.wait_for_timeout(5000)
        sleep(10) 
        
        err_counter: list[int] = [0,0]
        console = Console()
        lenght = len(songs_urls)

        with Progress() as progress:
            task1 = progress.add_task("Downloading", total=lenght)
            task2 = progress.add_task("Failed downloads", total=lenght)
            for index,i in enumerate(songs_urls):
                progress.update(task1, advance=1, description="Downloading tab %i of %i" % (index, lenght)) 
           
                try:
                    await page.goto(i['URL'])
                    await page.click('#revisions-toggle-tab') # Click in tab versions
                    # await page.reload()
                    await page.wait_for_selector('#download-link') # Wait for the selector
                    elements = await page.query_selector_all('#download-link') # Get all 'download' buttons

                    hrefs = [await i.get_attribute('href') for i in elements] # Get the urls of the gp tablature 
                
                    if hrefs != None: await download(i['Artist'], i['Title'], hrefs[0], path)
                    err_counter[0] = 0
                except: 
                    err_counter[0]+=1; err_counter[1]+=1
                    progress.update(task2, advance=1, description="Failed downloads %i of %i" % (err_counter[1], lenght))
                    if err_counter == 5: raise Exception("5 consecutive tabs failed downloading, try a new email")

        await browser.close()

async def download(artist: str, title: str, url: str, path: str) -> None:
    os.makedirs(os.path.join(path, f'Songsterr_tabs_extractor/{artist}'), exist_ok=True)
    subprocess.run(["wget", url, "-O", os.path.join(path, f"Songsterr_tabs_extractor/{artist}/{artist} - {title}.{url.split('/')[-1].split('.')[-1]}")],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True) 

async def create_songs_urls(json_path: str) -> list[str]:
    with open(os.path.join(json_path), 'r') as f: songsterr_data = json.load(f)
    
    data: list[str] = []

    for i in songsterr_data['favorites']:
        data.append({
            'Artist': i['artist'].capitalize(),
            'Title': i['title'].capitalize(), 
            'URL':"https://www.songsterr.com/a/wsa/%s-%s-tab-s%i" % (i['artist'].lower(), i['title'].lower().replace(' ', '-'), i['songId'])})
    return data

async def main() -> None:
    console = Console()
    if len(sys.argv) != 4: console.print("usage:\n\t%s <temp mail> <json path> <path to save>" % sys.argv[0]); sys.exit(1)
    elif not os.path.isfile(os.path.join(sys.argv[2])): console.log("JSON not found"); sys.exit(1)
    elif not os.path.isdir(os.path.join(sys.argv[3])): console.log("Directory not found"); sys.exit(1)
    else: await get_tabs_urls(str(sys.argv[1]), await create_songs_urls(str(sys.argv[2])), str(sys.argv[3]))
    # else: await create_songs_urls()
#
if __name__ == '__main__': asyncio.run(main()) 
