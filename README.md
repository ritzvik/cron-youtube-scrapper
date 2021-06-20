# Youtube Scrapper

## Getting started

### Prerequisite Software

| **No** | **Name**           | **Version** | **Notes**                                                                        |
| ------ | ------------------ | ----------- | -------------------------------------------------------------------------------- |
| 1      | Python               | 3.8          |
| 2      | Postgres             | 12.0          |
| 3    | Docker             | **Latest**  |

### Start application locally

```docker
docker-compose up
```

### Run tests
```docker
docker-compose up code_service_test
```

## Secrets File
  - The config file is `config/app_secrets/common_settings.yml`. I would generally gitignore it, and not push it to the repo, but doing it here for the time being.
  - You can modify the search term on youtube and the used API keys in the config file. They are named `youtube_query_string` and `youtube_keys` respectively.

## API Docs
  - API documentation can be accessed [here](http://localhost:3012/api-docs) when docker is running. APIs can be tried out there directly from the browser.

## Simple GET API
  - curl command
    ```
    curl -X GET "http://localhost:3012/v1/scrapper/videos/?items=2&page=1&q=upi%20fampay" 
    ```
  - You would need to wait about a minute after docker is running, so as to let the cron populate the DB (if at all the API keys have not exhausetd the quota).
  - paramters `items` is the number of item per page, `page` is the page number requested and `q` is the search string. All parameters are optional

## Optional questions attempted in this assignment 
  - Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
  - Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.
     - Ex 1: A video with title *`How to make tea?`* should match for the search query `tea how`

## Miscellaneus Info
  - Using django as backend framework.
  - core logic of the youtube scrapper can be found in the `scrapper` django app.
  - celery is used for async tasks and crons
  - crons can be found in `scrapper/tasks.py`
  - crons are trigerred every 1 minute, which in turn queue youtube scrapping tasks every 10 seconds. This hack is done because, 1 minute is the lowest amount taken as input by crontab.
  - project is using swagger for API docs generation.
## Style Guides

- [PEP8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
