from selenium import webdriver
from time import sleep
import re
import youtube_dl
import pathlib


def check_url(url):
    if 'youtube.com/playlist?' in url:
        get_inspect(url)
    elif 'youtube.com/watch?v' in url:
        with open('vid_links.txt', 'a', encoding='utf-8') as txt_file:
            txt_file.write('\n' + url)

def get_inspect(url):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    sleep(3)
    try:
        driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span').click()
    except:
        pass
    html1 = driver.page_source
    html2 = driver.execute_script("return document.documentElement.innerHTML;")
    vid_ids = re.findall('(/watch\?v=.*index=\d*)\"', html2)
    with open('vid_links.txt', 'w', encoding='utf-8') as my_file:
        str_of_vid_ids = ''
        for vid_id in vid_ids[2:-1]:
            if vid_id in str_of_vid_ids:
                continue
            else:
                str_of_vid_ids += 'https://www.youtube.com' + vid_id + '\n'
        my_file.write(str_of_vid_ids)

def dl_video_list():
    current_dir = pathlib.Path().resolve()
    txt_file = open('vid_links.txt', 'r', encoding='utf-8')
    link_list = txt_file.readlines()
    txt_file.close()
    download_list = link_list.copy()
    dir_name = 'Utube Playlist Downloader'
    for link in download_list:
        if 'youtube.com/watch?v=' in link:
            if 'index=' in link:
                index = re.search('index=(\d*)', link).groups()[0]
                ydl_opts = {
                    'outtmpl': str(current_dir) + f'/{dir_name}/{index}- %(title)s.%(ext)s',
                }
            else:
                ydl_opts = {
                    'outtmpl': str(current_dir) + f'/{dir_name}/%(title)s.%(ext)s',
                }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            link_list.pop(link_list.index(link))
            txt_file = open('vid_links.txt', 'w', encoding='utf-8')
            for link in link_list:
                txt_file.write(link)
            txt_file.close()
        else:
            continue
            
def check_resume():
    txt_file = open('vid_links.txt', 'r+', encoding='utf-8')
    link_list = txt_file.readlines()
    txt_file.close()
    while len (link_list) > 0:
        while True:
            answer = input('You have an unfinished dl list. Do you want resume it? [y/n] ').lower()
            if answer == 'y':
                dl_video_list()
                break
            elif answer == 'n':
                url = input('Video or playlist url: ')
                check_url(url)
                dl_video_list()
                break
            else:
                print('Invalid input')
    else:
        url = input('Video or playlist url: ')
        check_url(url)
        dl_video_list()

def main():
    try:
        check_resume()
    except FileNotFoundError:
        open('vid_links.txt', 'w', encoding='utf-8').close()
        check_resume()


if __name__ == '__main__':
    main()