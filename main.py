from selenium import webdriver
from time import sleep
import re
import youtube_dl
import pathlib


def check_url(url, dir_name='Utube Playlist Downloader'):
    if 'youtube.com/' in url or 'youtu.be/' in url:
        is_playlist = re.findall('(/playlist\?list=.{34})', url)
        is_video = re.findall('(/watch\?v=.{11})', url) or re.findall('youtu\.be/(.{11})', url)
        find_playlist_id = re.findall('(list=.{34})', url)
        if is_playlist:
            get_inspect(url, dir_name)
            print('All videos in playlist added to download list.')
        elif is_video:
            if find_playlist_id:
                print('This video is from a youtube playlist.')
                while True:
                    answer = input('Do you want to download playlist [y] or just this video [n]? ').lower()
                    if answer == 'y':
                        playlist_url = 'https://www.youtube.com/playlist?' + find_playlist_id[0]
                        get_inspect(playlist_url, dir_name)
                        print('All videos in playlist added to download list.')
                        break
                    elif answer == 'n':
                        video_url = 'https://www.youtube.com' + is_video[0] + '\n'
                        with open('vid_links.txt', 'a', encoding='utf-8') as txt_file:
                            txt_file.write(f'\n{dir_name}\n' + video_url)
                        print('Video added to download list.')
                        break
                    else:
                        print('Invalid input. Just enter "y" or "n".')
            else:
                with open('vid_links.txt', 'a', encoding='utf-8') as txt_file:
                    txt_file.write(f'\n{dir_name}\n' + url)
        else:
            print('Not found. Maby your link is invalid.')
    else:
        print('Invalid Youtube Link.')

def get_inspect(url, dir_name):
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
    with open('vid_links.txt', 'a', encoding='utf-8') as my_file:
        str_of_vid_links = f'\n{dir_name}\n'
        for vid_id in vid_ids[2:-1]:
            if vid_id in str_of_vid_links:
                continue
            else:
                str_of_vid_links += 'https://www.youtube.com' + vid_id + '\n'
        my_file.write(str_of_vid_links)

def dl_video_list():
    current_dir = pathlib.Path().resolve()
    txt_file = open('vid_links.txt', 'r', encoding='utf-8')
    link_list = txt_file.readlines()
    txt_file.close()
    download_list = link_list.copy()
    dir_name = 'Utube Playlist Downloader'
    for link in download_list:
        if link != '\n':
            if 'youtube.com/watch?v=' not in link:
                dir_name = link[:-1]
            elif 'youtube.com/watch?v=' in link:
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
    all_str = ''
    for link in link_list:
        all_str += link
    while len (link_list) > 0:
        if 'https://www.youtube.com' in all_str:
            while True:
                answer = input('Start Download? [y/n] ').lower()
                if answer == 'y':
                    dl_video_list()
                    print('video(s) added to download list.')
                    break
                elif answer == 'n':
                    url = input('Video or playlist url: ')
                    dir_name = input('Enter a folder name to save videos:')
                    check_url(url, dir_name)
                    break
                else:
                    print('Invalid input')
        else:
            with open('vid_links.txt', 'w', encoding='utf-8') as txt_file:
                txt_file.write('')
            url = input('Video or playlist url: ')
            dir_name = input('Enter a folder name to save videos:')
            check_url(url, dir_name)
            
    else:
        url = input('Video or playlist url: ')
        dir_name = input('Enter a folder name to save videos:')
        check_url(url, dir_name)
        dl_video_list()

def main():
    try:
        check_resume()
    except FileNotFoundError:
        open('vid_links.txt', 'w', encoding='utf-8').close()
        check_resume()


if __name__ == '__main__':
    main()