# Ansible collection

Ansible collection 입니다.

Collection 개발 방법에 대한 내용은 https://docs.ansible.com/ansible/2.9/dev_guide/developing_collections.html 를 참고해 주세요.


# Setup

1. 프로젝트 클론
```sh
$ git clone https://git.monitorapp.com/qa/ansible/collection
```

2. Ansible 다운로드 (20/28/12기준 2.9.16)
```sh
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
```
> 원본 가이드 : https://docs.ansible.com/ansible/2.9/installation_guide/intro_installation.html#installing-ansible-on-ubuntu

3. ansible-test 모듈 설치
```sh
$ sudo apt-get install ansible-test
```

4. Python 모듈 설치
```sh
$ sudo apt-get install python python3 python-pip python3-pip
$ sudo pip3 install 
$ sudo pip3 install pyyaml pycodestyle pylint voluptuous psycopg2 jinja2
```

# ansible-test

1. 해당 폴더로 이동
```sh
$ cd ansible_collections/monitorapp/monitorapp_waf
```
2. 테스트 실행
```sh
$ sudo ansible-test sanity
```

