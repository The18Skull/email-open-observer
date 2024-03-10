# Email open observer

A simple app which sends an email and monitors recepient to open it.


## Config

Example of _config.yml_ content:

```yaml
host: example.com
gmail:
  login: login@gmail.com
  password: password
  from: login@gmail.com
```


## Schema

This app uses sqlite connection to store data with schema:

| Column      | Type     | Description                       |
| ----------- | -------- | --------------------------------- |
| uid         | UUID     | Unique recepuent's id             |
| iid         | UUID     | Unique url's id to "real" image   |
| email       | TEXT     | Recepient's email                 |
| timestamp   | DATETIME | Timestamp when message was opened |


## Logic

There are two types of UUIDs:

* UUID v4 for storing unique user ids.
* UUID v3 for storing unique path to "real" image which will be shown after user do any action we want. For this demo it is to simply open this email once.

---

1. Start a web server via `serve` command.

It listens to any http request to any path. Any request which can not be converted to UUID type returns 404. Otherwise it checks if UUID is known. If UUID is v4 it updates timestamp for this user in DB. If UUID is v3 and record with this UUID has timestamp it returns "real" image otherwise 404.

2. Send an email to target via `send --address <email>` command.

This command generates a pair of UUID v4 and UUID v3 then renders email's body and sends it. All data is stored to DB.

_For now it uses only gmail accounts to send emails._


## Epilogue

This app was made as a small pet-project to prove a point and to test how such messages really work.
It **was not** used and **was not** intended to be used to blackmail or intimidate anybody.
