BOJ Auto-Submit for mac
=====================

## 1. 실행방법

```
$ python3 .setup.py install
$ python3 .submit.py [problem_number.cpp]
```	
OR
```
$ python3 .setup.py install
$ alias submit='python3 .submit.py'
$ submit [problem_number.cpp]
```

* 1000.cpp 파일로 테스트해보세요.
* C/C++로 작성 된 소스코드만 제출이 가능합니다.
* 제출할 소스코드가 .submit.py와 같은 경로에 있어야 합니다.
* 첫 제출 이후에는 쿠키가 저장되어 더 빠르게 작동합니다.

## 2. Chromedriver가 Permission error가 날 경우

```
chmod a+x driver/chromedirver_linux
```

## 3. Dependency
	1. Python3
	2. requests
	3. selenium
	4. bs4
	5. Chrome
