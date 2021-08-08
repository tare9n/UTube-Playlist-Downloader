from selenium import webdriver
from time import sleep
import re
import youtube_dl
import pathlib


def get_inspect(url):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    sleep(3)
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span').click()
    html1 = driver.page_source
    html2 = driver.execute_script("return document.documentElement.innerHTML;")
    vid_ids = re.findall('(/watch\?v=.{11})', html2)
    with open('vid_links.txt', 'w', encoding='utf-8') as my_file:
        str_of_vid_ids = ''
        for vid_id in vid_ids[3:]:
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
    for i, link in enumerate(download_list):
        ydl_opts = {
            'outtmpl': str(current_dir) + f'/{dir_name}/{i+1}- %(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        link_list.pop(link_list.index(link))
        txt_file = open('vid_links.txt', 'w', encoding='utf-8')
        for link in link_list:
            txt_file.write(link)
        txt_file.close()
            

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
                playlist_link = input('New playlist link: ')
                get_inspect(playlist_link)
                dl_video_list()
                break
            else:
                print('Invalid input')
    else:
        playlist_link = input('New playlist link: ')
        get_inspect(playlist_link)
        dl_video_list()


def main():
    try:
        check_resume()
    except FileNotFoundError:
        txt_file = open('vid_links.txt', 'w', encoding='utf-8')
        txt_file.close()
        check_resume()


if __name__ == '__main__':
    main()
