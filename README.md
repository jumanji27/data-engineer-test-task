Run containers with DBs:

`docker-compose up --build --force-recreate -d hb_db wwc_db`

When they are ready, run the parser container:

`docker-compose up --build --force-recreate normalizer`

To configure the type of game, change `./configs/normalizer.yml` `type` field and run the container again.

To get access to DBs, see `./configs/normalizer.yml` `dbs` list.

To run tests (will work only after normalizer run)

`docker-compose up --build --force-recreate tests`

**Important notes**:
  - For the hb dataset, it is possible to detect user location by IP
    using an external service (ip2location.com, whatismyipaddress.com). I didn't do it deliberately because it's inaccurate, requires external dependencies, and I don't think it's part of the task
  - I used only data tests to check my code. I think it's enough to fit the correctness of the codebase in that case.
    I deliberately missed unit tests here.
  - As for the data pipeline for user events, it's a completely different task.
    For that type of data, I would prefer to use time series databases
    like TimescaleDB, InfluxDB, or AWS Timestream.
    They can easily write a massive amount of time-indexed records (like events),
    but they're slow in complicated queries than we want to read and aggregate our data.
    If we want fast performance in both reading and writing, we need to set up something like HDFS and MapReduce.
    Not sure about principles, but I think these are important:
    - It's important to write fast, you can wait or be inaccurate in reads
    - Fresh data is more important than old. You can thin out old data.
    - Use queue services like Kafka or Rabbit can save you a lot of time.