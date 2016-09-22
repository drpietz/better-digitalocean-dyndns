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
