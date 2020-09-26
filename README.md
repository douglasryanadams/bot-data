This repo contains code that's used for building simple nginx servers to capture bot traffic and pulling down logs from the servers in an automated fashion.

If this collects enough data, I'm going to use it to train some machine learning tools to detect bots (in theory).



We'll serve as many of these combinations from each VPS as we can
They'll have separate log files for each type of connection, if possible

| ID  | IPv | Domain | HTTPS |
| --- | --- | ------ | ----- |
| 1   | 4   | -      | -     |
| 2   | 4   | x      | -     |
| 3   | 4   | x      | x     |
| 4   | 6   | -      | -     |
| 5   | 6   | x      | -     |
| 6   | 6   | x      | x     |

We'll have Hosts purchased from:

- vultr
- arubacloud
- ramnode

I'm hoping that these cheap servers will be cost effective and also have less bot-blocking firewall stuff than larger names like DigitalOcean or AWS

Future Goals:
- Serve up Fingerprinting JS to store that data too if we're hit by browsers

