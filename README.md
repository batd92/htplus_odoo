# Installing Odoo 18.0

## Custom addons

The **addons/** folder contains custom addons. Just put your custom addons if you have any.

## Odoo configuration & log

* To change Odoo configuration, edit file: **odoo.conf**.
* Log file: **etc/odoo-server.log**
* Default database password (**admin_passwd**) is `htadmin@123`, please change it @ [/odoo.conf#L60](/odoo.conf#L60)

## Odoo container management

**Run Odoo**:

``` bash
docker-compose up -d
```

**Restart Odoo**:

``` bash
docker-compose restart
```

**Stop Odoo**:

``` bash
docker-compose down
```

## Services in `docker-compose`

* odoo:18
* postgres:17
* nginx


- **If you get any permission issues**, change the folder permission to make sure that the container is able to access the directory:

``` sh
$ sudo chmod -R 777 addons
$ sudo chmod -R 777 etc
$ sudo chmod -R 777 volumes
```

#### Open HRMS HR Dashboard
To install the required dependencies within the `odoo` container, please execute the following command inside the container:

```python3 -m pip install pandas --break-system-packages```

Dashboard: 
======

```http://localhost/```

<img width="1321" alt="image" src="https://github.com/user-attachments/assets/6478c4ec-0017-4af5-9420-33c62e79fae0" />
