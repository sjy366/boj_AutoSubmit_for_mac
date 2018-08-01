import sys
import getpass
import requests
import platform
import pickle
from selenium import webdriver
from bs4 import BeautifulSoup as bs

url = "https://www.acmicpc.net"

USER_INFO = {
    'id': '',
    'pw': ''
}

result = {
    '맞았습니다!!',
    '출력 형식이 잘못되었습니다', '틀렸습니다', '시간 초과',
    '메모리 초과', '출력 초과', '런타임 에러', '컴파일 에러'
}

set_cookie_flag = False

# Input user data
with open("./.data/user.dat", 'r') as f:
    data = f.readline().split()
    if len(data) == 0:
        with open("./.data/user.dat", 'w') as f:
            id_str = input("\nUser ID:")
            pw_str = getpass.getpass("User PW:")
            f.write(id_str + ' ' + pw_str)
            USER_INFO['id'] = id_str
            USER_INFO['pw'] = pw_str
            print()
            set_cookie_flag = True
    else:
        USER_INFO['id'] = data[0]
        USER_INFO['pw'] = data[1]

if set_cookie_flag:
    # Set driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    os_name = platform.system()
    if os_name == "Windows":
        driver = webdriver.Chrome('./.driver/chromedriver_win.exe', chrome_options=options)
    elif os_name == "Darwin":
        driver = webdriver.Chrome('./.driver/chromedriver_mac', chrome_options=options)
    elif os_name == "Linux":
        driver = webdriver.Chrome('./.driver/chromedriver_linux', chrome_options=options)

    # Login by driver
    driver.get(url + "/login")
    driver.find_element_by_name('login_user_id').send_keys(USER_INFO['id'])
    driver.find_element_by_name('login_password').send_keys(USER_INFO['pw'])
    driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/form/div[4]/div[2]/button").click()
    cookies = driver.get_cookies()
    with open("./.data/cookie.dat", 'wb') as f:
        pickle.dump(cookies, f)
else:
    with open("./.data/cookie.dat", 'rb') as f:
        cookies = pickle.load(f)

# Set cookies
sess = requests.Session()
for cookie in cookies:
    sess.cookies.set(cookie['name'], cookie['value'])

# Login check
soup = bs(sess.get(url).text, 'html.parser')
if soup.find('a', {'class': 'username'}) is None:
    print("\nLogin failed : Invalid ID or Password.")
    sys.exit()

# Make code
filename = sys.argv[1]
tmp = filename.split('.')
problem_number = tmp[0]

submit_code = ""
with open(filename, 'r') as f:
    for line in f:
        submit_code += line

# Submit code
soup = bs(sess.get(url + "/submit/" + problem_number).text, 'html.parser')
key = soup.find('input', {'name': 'csrf_key'})['value']

data = {
    'problem_id': problem_number,
    'language': '49',
    'code_open': 'open',
    'source': submit_code,
    'csrf_key': key
}
sess.post(url + "/submit/" + problem_number, data=data)

# Print result
done = False
while not done:
    _url = url + "/status?from_mine=1&problem_id=" + problem_number + "&user_id=" + USER_INFO['id']
    soup = bs(sess.get(_url).text, 'html.parser')
    text = soup.find('span', {'class': 'result-text'}).find('span').string.strip()
    print("\r                          ", end='')
    print("\r%s" % text, end='')
    if text in result:
        done = True
print()
