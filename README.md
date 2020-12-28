# Ansible collection

Ansible collection 입니다.

Collection 개발 방법에 대한 내용은 https://docs.ansible.com/ansible/2.9/dev_guide/developing_collections.html 를 참고해 주세요.


# Setup
## HOST

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
$ sudo pip3 install pyyaml pycodestyle pylint voluptuous psycopg2 jinja2
```

5. SSH 연결 설정 (패스워드 없이 로그인)
```sh
$ sudo ssh-keygen -t rsa
$ sudo scp ~/.ssh/id_rsa.pub {USER}@{HOST}:~/.ssh/authorized_keys
$ sudo ssh-copy-id -i ~/.ssh/id_rsa.pub {USER}@{HOST}
```

6. hosts에 Client IP 추가 (nano, vi...)
```sh
$ sudo nano /etc/ansible/hosts
```
> 맨 하단에 IP 추가하면 됩니다.

## Client

1. Python 모듈 설치
```sh
$ sudo apt-get install python python3 python-pip python3-pip
$ sudo pip3 install 
$ sudo pip3 install psycopg2 requests
```

2. API Open (WEB UI)


# ansible-test (HOST)

1. 해당 폴더로 이동
```sh
$ cd ansible_collections/monitorapp/monitorapp_waf
```

2. 테스트 실행
```sh
$ sudo ansible-test sanity
```

# ansible-playbook (HOST)

1. 모듈 Path 추가 (nano, vi...)
```sh
$ sudo nano /etc/ansible/ansible.cfg
```
> [defaults]의 library 값에 module path 추가하면 됩니다

2. data/vars.json 내 계정 정보 추가 (nano, vi...)
```sh
$ sudo nano ansible_collections/monitorapp/monitorapp_waf/data/vars.json
```
> db.id, db.password => postgres db 계정정보
> 
> web.id, web.password => 관리자 WEB(222) 계정정보
>
> 각 모듈들에 대한 파라미터값은 모두 var.json에 설정 되어있습니다. 예시값으로 설정 되어 있으니 필요에 따라 수정하여 사용 하시면 됩니다.

- example
```sh
$ sudo cd ansible_collections/monitorapp/monitorapp_waf
$ sudo ansible-playbook playbook/login.yml --extra-vars '@./data/vars.json'
$ sudo ansible-playbook playbook/whitelist.yml --extra-vars '@./data/vars.json'
```
> 모든 playbook 실행 전 login.yml 최초 1회 실행이 필요 합니다. (API login)
