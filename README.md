# Device Registry Service

## Usage

All responses will have the form

```json
{
  "data": "Mixed type holding the content of the response",
  "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all devices

**Definition**

`GET /devices/all`

**Response**

- `200 Ok` on success

```json
[
  {
    "identifier": "floor-lamp",
    "name": "Floor lamp",
    "device_type": "switch",
    "controller_gateway": "192.168.0.2"
  },
  {
    "identifier": "samsung-tv",
    "name": "Samsung TV",
    "device_type": "tv",
    "controller_gateway": "192.168.0.9"
  }
]
```

### Registering a new device

**Definition**

`POST /device`

**Arguments**

- `"identifier":string` a globally unique identifier for this device
- `"name":string` a friendly name for this device
- `"device_type":string` the type of device as understood by the client
- `"controller_gateway":string` the IP address of the device's controller

If a device with a given identifier already exists, the device will be overwritten

**Response**

- `201 Created` on success

```json
{
  "identifier": "floor-lamp",
  "name": "Floor lamp",
  "device_type": "switch",
  "controller_gateway": "192.168.0.2"
}
```

### Lookup device details

`GET /devices?identifier=<identifier>`

**Response**

- `404 Device not found` if device does not exist
- `200 OK` on success

```json
{
  "identifier": "floor-lamp",
  "name": "Floor lamp",
  "device_type": "switch",
  "controller_gateway": "192.168.0.2"
}
```

### Delete device

`DELETE /device?identifier=<identifier>`

**Response**

- `404 Device not found` if device does not exist
- `200 OK` on success

---

## Troubleshooting Notes

### docker-compose errors on Ubuntu

When spinning up this system on local environment running:

- Ubuntu 19.10
- Docker 19.03.6

  Error:

  _NewConnectionError('<pip.\_vendor.urllib3.connection.HTTPSConnection object..._

**Issue Summary**

DNS related issue when docker compose begins installing requirements. Resolution was to create a daemon file and add the dev system's DNS.

**Resolution**

Get a valid DNS for local system:

```
nmcli dev show | grep 'DNS'
```

Create daemon file and add DNS:

```
sudo nano /etc/docker/daemon.json
```

Add content:

```
{
	"dns": ["172.16.10.2"]
}
```

Restart docker service:

```
sudo service docker restart
```

**Reference**

[StackOverflow Resolution](https://stackoverflow.com/questions/28668180/cant-install-pip-packages-inside-a-docker-container-with-ubuntu/41989423#41989423S)
