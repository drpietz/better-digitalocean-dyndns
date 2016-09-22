# digitalocean-dyndns
Fully automated and customizable python script for using DigitalOcean as a DynDNS service.

## Configuration
Example Configuration json file:
```
{
  "bearers": [
    {
      "key": "b7d03a6947b217efb6f3ec3bd3504582",
      "domains": [
        {
          "name": "example.com",
          "dyn_records": [
            {
              "name": "sub1",
              "type": "A",
              "device": "raspi"
            },
            {
              "name": "sub2",
              "device": "raspi"
            }
          ]
        },
        {
          "name": "me.io",
          "dyn_records": [
            {
              "name": "@",
              "type": "TXT",
              "data": "current ip: %4",
              "device": "raspi"
            }
          ]
        }
      ]
    },
  ]
}
```

### Dynamic records
You have to create an entry in the `dyn_records` array for each DNS record you want to update dynamically. Each of these entries may contain the following attributes:

`name` to specify the subdomain.

`type` to specify the domain record type that is to be updated.  
If not present, both the A and the AAAA records will be updated, unless `data` is set, in which case `type` will default to `TXT`.

`data` can be used to format the data before sending it to DigitalOcean.  
Optional for A and AAAA records.  
You can use `%v4` to insert the IPv4 address and `%v6` for the IPv6 address respectively. Use `%%` to insert a literal %.

`device` is used as an identifier to determine wheter a device is supposed to handle dynamic IP updates for this record.

## Handling multiple devices
You can use the device property of dynamic records to specify the name of the device, which is supposed to handle dns updates for this record.
