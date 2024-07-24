Это документация непосредственно на интерфейс Робо7 его установку и использование

Содержание
1. Установить виртуальную машину VM Virtualbox или развернуть из образа
2. Настроить проброс портов во внешней систему
3. Выполнить Git clone для репозитория интерфейса
    sudo git clone https://github.com/edemura/roboweb.git
4. Установить Portainer (учетные данные: admin:portaineradmin)
    sudo docker volume create portainer_data
    sudo docker run -d -p 8002:8002 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
    https://localhost:9443/
5. 
