# Проверка версии и загрузка + распоковка
# бомже девопс :)
import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os 
# # Установка переменной окружения перед использованием GitPython
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git

url = "https://github.com/disc0nn3ct/buffer_project"

st_accept = "text/html" # говорим веб-серверу, 
                        # что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

def take_ver(ver_from_str):
    return list(filter(str.isdigit, ver_from_str))


def request_ver(url_v):
    req = requests.get(url_v, headers)
    print("Статус ответа сайта = ", req.status_code)
    return req



def uznat_tegi():
    full_url = url + "/blob/main/version.ver"
    req = request_ver(full_url)    
    soup = BeautifulSoup(req.text, 'lxml')

    for child in soup.recursiveChildGenerator():
        if child.name:
            print(child.name)



def check_version():
    full_url = url + "/blob/main/version.ver"
    req = request_ver(full_url)
    # print(full_url)
    soup = BeautifulSoup(req.text, "html.parser")
    # soup = BeautifulSoup(req.text, 'lxml')

    ver_url = re.search(r"(?<=\"rawLines\"\:\[\").*?(?=\"\])", str(soup)).group(0)
    return take_ver(ver_url)

    # allNews = soup.findAll('rawLines')
    # print(allNews)


    #span data-code-text

# сравнение версий из github и настоящей, вернет 1, если версия на гит больше, чем та, что скачена
def compare_ver(ver_cur, ver_url):
    if ver_cur[0] < ver_url[0] or (ver_cur[0] == ver_url[0] and ver_cur[1] < ver_url[1]):
        return 1  # обновить
    elif ver_cur == ver_url:
        return 0  # актуальная
    else:
        return -1  # версия cur > версии url
    
# def compare(ver_cur, ver_url):
#     if ver_cur[0] < ver_url[0]:
#         return 1 # обновить
#     else:
#         if ver_cur[0] == ver_url[0]:
#             if ver_cur[1] == ver_url[1]:
#                 return 0 # акутальная
#             else:
#                 if ver_cur[1] > ver_url[1]:
#                     return -1 # ??
#                 else:
#                     return 1

#         if ver_cur[0] > ver_url[0]:
#             return -1 # что случилось?

# content = os.listdir(example_dir)
# images = []
# for file in content:
#     if os.path.isfile(os.path.join(example_dir, file)) and file.endswith('.jpg'):
#         images.append(file)    


# Проверить версии скаченные в директории. И вернуть максимальную скаченную версию 
def take_latest_from_dir():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    content = os.listdir()
    print(content)

    cur_dirs = []
    for file in content:
        if os.path.isdir(os.path.join(cur_path, file)):
            cur_dirs.append(file)
    print(cur_dirs)

    vers = []
    for file in cur_dirs:
        vers.append(take_ver(file))
    mas_ver=vers[0]
    
    for i in vers:
        if compare_ver(mas_ver, i)==1:
            mas_ver=i

    # print('max =', mas_ver)
    return mas_ver


    





def current_ver():

    current_ver_file = open('version.ver','r')

    cur_ver = take_ver(str(current_ver_file.readlines()))
    # print(cur_ver)
    current_ver_file.close()
    return cur_ver



def download_latest_version(repo_url):
    cur_ver = check_version()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path + "\\" + cur_ver[0] + "_" + cur_ver[1]
    # print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)   
    
    try:
        repo = git.Repo(dir_path)
        origin = repo.remotes.origin
        origin.pull()
    except git.exc.InvalidGitRepositoryError:
        git.Repo.clone_from(repo_url, dir_path)


# Пример использования
# repository_url = "https://github.com/owner/repository.git"
# destination_folder = "/path/to/destination"

def start_latest():
    name_of_project = "parsing test" # проект из пула  
    latest_ver = take_latest_from_dir()
    #todo проверку версии
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path + "\\" + latest_ver[0] + "_" + latest_ver[1] + "\\" + name_of_project
    os.chdir(dir_path)
    # print("dir_path", dir_path)
    content = os.listdir('.')
    # print(content)
    py_file = []
    for file in content:
        if os.path.isfile(os.path.join(dir_path, file)) and file.endswith('.py'):
            py_file.append(file)
    # print("./" + py_file[0])

    subprocess.call(['python', py_file[0] ])
    # subprocess.call("./" + py_file[0], shell=True)


download_latest_version(url)


# print(os.path.dirname(os.path.realpath(__file__)))
# cwd = os.getcwd()

# print(os.getcwd())

# if current_ver() < check_version():
#     reload()




print(check_version())

print(current_ver())


print(compare_ver(current_ver(), check_version()))

start_latest()




