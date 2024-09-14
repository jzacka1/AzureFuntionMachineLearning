import azure.functions as func
import logging
import numpy
import json
from scipy import stats

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="az_func_ml")
def az_func_ml(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
@app.route(route="mean_median_mode")
def mean_median_mode(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = req.get_body()

    if not body:
        try:
            req_body = req.get_json()
            data = json.loads(req_body)
        except ValueError:
            pass

    data = json.loads(body)

    # speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]

    median = numpy.median(data)
    mean = numpy.mean(data)
    mode = stats.mode(data).mode
    modeCount = stats.mode(data).count

    if median and mean and mode:
        return func.HttpResponse(f"The median value of the values you provided is: {median} \n The mean is: {mean} \n The mode is {mode}, and it appeared {modeCount} times")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )