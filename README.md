## Deployment instructions
* install docker https://www.docker.com/get-started
* in project's base directory run `docker-compose up -d` to start api

## Endpoint
* `http://[host]:5000/api/hyperdrive/`, method GET

Please see "sample" folder for Postman examples.

## Assumptions
1. When at least one single network call fails, no results are displayed.
2. For sake of simplicity, no production web server
