# GET
curl http://localhost/bookjobs

# POST
curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "job id 4"}' \
    http://localhost/bookjobs

# GET specific id
curl http://localhost/bookjobs/4

# DELETE - must provide id
curl -X "DELETE" http://localhost/bookjobs/4