# better-digitalocean-dyndns
Fully automated and customizable python script for using DigitalOcean as a DynDNS service.

## Configuration
Example config.json file:
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
              "host": "raspi"
            },
            {
              "name": "sub2",
              "host": "raspi"
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
              "host": "raspi"
            }
          ]
        }
      ]
    },
  ]
}
```

Example config.ini file:
```
[Dodns]
Hostname=raspi
Interval=300
```

### Dynamic records
You have to create an entry in the `dyn_records` array for each DNS record you want to update dynamically. Each of these entries may contain the following attributes:

`name` to specify the subdomain.

`type` to specify the domain record type that is to be updated.  
If not present, both the A and the AAAA records will be updated, unless `data` is set, in which case `type` will default to `TXT`.

`data` can be used to format the data before sending it to DigitalOcean.  
Optional for A and AAAA records.  
You can use `%v4` to insert the IPv4 address and `%v6` for the IPv6 address respectively. Use `%%` to insert a literal %.

`host` is used as an identifier to determine whether a host is supposed to handle dynamic IP updates for this record.  
If not present, any host will update the record.

## Handling multiple hosts
You can use the host property of dynamic records to specify the name of the host, which is supposed to handle DNS updates for this record.  
By default, the value of `os.gethostname()` is used, but can be changed in the config.ini.
