import sys
import getpass
import requests
from bs4 import BeautifulSoup as bs

url = "https://www.acmicpc.net"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
    'Referer': url,
    'Origin': url
}

USER_INFO = {
    'id': '',
    'pw': ''
}

result = {
    '맞았습니다!!',
    '출력 형식이 잘못되었습니다', '틀렸습니다', '시간 초과',
    '메모리 초과', '출력 초과', '런타임 에러', '컴파일 에러'
}

sess = requests.Session()

def load_user_data():
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
        else:
            USER_INFO['id'] = data[0]
            USER_INFO['pw'] = data[1]

def sign_in():
    data = {
        'login_user_id': USER_INFO['id'],
        'login_password': USER_INFO['pw']
    }
    sess.post(url + "/signin", headers=headers, data=data)

def is_invalid_login():
    soup = bs(sess.get(url, headers=headers).text, 'html.parser')
    if soup.find('a', {'class': 'username'}) is None:
        print("Login failed : Invalid ID or Password.")
        with open("./.data/user.dat", 'w') as f:
            f.write('')
        return True
    else:
        return False

def load_code(filename):
    submit_code = ""
    with open(filename, 'r') as f:
        submit_code = f.read()
    return submit_code

def submit(problem_number, submit_code, language):
    soup = bs(sess.get(url + "/submit/" + problem_number, headers=headers).text, 'html.parser')
    key = soup.find('input', {'name': 'csrf_key'})['value']
    language_code = 49 # default: c++

    if language == '.cpp' or language == '.cc':
        language_code = 49
    elif language == '.py':
        language_code = 28
    elif language == '.java':
        language_code = 3
    elif language == '.txt':
        language_code = 58
    elif language == '.js':
        language_code = 17

    data = {
        'problem_id': problem_number,
        'source': submit_code,
        'language': language_code,
        'code_open': 'open',
        'csrf_key': key
    }
    sess.post(url + "/submit/" + problem_number, headers=headers, data=data)

def print_result(problem_number):
    done = False
    while not done:
        _url = url + "/status?from_mine=1&problem_id=" + problem_number + "&user_id=" + USER_INFO['id']
        soup = bs(sess.get(_url, headers=headers).text, 'html.parser')
        text = soup.find('span', {'class': 'result-text'}).find('span').string.strip()
        print("\r                          ", end='')
        print("\r%s" % text, end='')
        if text in result:
            done = True
    print()

if __name__ == "__main__":
    filename = sys.argv[1]
    tmp = filename.split('.')
    problem_number = tmp[0]
    language = '.' + tmp[1]

    load_user_data()
    sign_in()

    if is_invalid_login():
        sys.exit()

    submit_code = load_code(filename)
    submit(problem_number, submit_code, language)
    print_result(problem_number)

    sess.close()
