# azkaban_py
Get status of azkaban jobs using [ajax web services](http://azkaban.github.io/azkaban/docs/latest/#ajax-api)

Outputs jobs that have failed

#Configuration

Change `AZKABAN_BASE_URL`, `AZKABAN_USERNAME`,`AZKABAN_PASSWORD` constants to the appropriate values

#Run:

`python azkaban_crawler.py`
    Starts from last saved job id or 0 if it is the first run

`python azkaban_crawler.py 123` 
    Starts from the specified job id
