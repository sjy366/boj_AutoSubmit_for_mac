BOJ Auto-Submit for mac
=====================

## 1. 실행방법

```
$ python .setup.py install
$ python .submit.py [problem_number.cpp]
```	
OR
```
$ python .setup.py install
$ alias submit='python3 .submit.py'
$ submit [problem_number.cpp]
```

* C/C++로 작성 된 소스코드만 제출이 가능합니다.
* 제출할 소스코드가 .submit.py와 같은 경로에 있어야 합니다.

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
