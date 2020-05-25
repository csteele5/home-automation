# Device Registry Service

## Usage

All responses will have the form

``` json
{
	"data": "Mixed type holding the content of the response",
	"message": "Description of what happened"
}
```
Subsequent response definitions will only detail the expected value of the `data field`

### List all devices

**Definition**

`GET /devices`

**Response**

- `200 Ok` on success

``` json
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

`GET /device?identifier=<identifier>`

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
```


