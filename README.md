An overengineered "where am I" using Tripit data.

# Set Up

I used foreman because Heroku. You'll need these env vars:

* `DATABASE_URL=postgres://localhost/flightlog-development`, or something along those lines
* `TRIPIT_OAUTH_KEY` and `TRIPIT_OAUTH_SECRET`, from [Tripit](https://www.tripit.com/developer/create)
* `TRIPIT_CONSUMER_KEY` and `TRIPIT_CONSUMER_SECRET`. Run setup.py, follow the instructions. `key` and
    `secret` should get spit out at the end.

Run the migrations with `foreman run python manage.py syncdb`
Scrape the data with `foreman run python manage.py scrape_tripit`.

# Deploying to Heroku
For Heroku, replace `foreman run` with `heroku run`
You may want to use Heroku Scheduler to scrape periodically.
