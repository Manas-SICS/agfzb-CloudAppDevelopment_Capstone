from cloudant.client import Cloudant
from cloudant.error import CloudantException


# main() will be run automatically when this action is invoked in IBM Cloud
def main(dict):

    secret = {
        "URL": "https://55e78b78-d769-452b-b437-52069b827068-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "3tN02_CVbex9EoiUmpbWV5ktsBLCxCzgH77fZtfiQQsn",
        "ACCOUNT_NAME": "55e78b78-d769-452b-b437-52069b827068-bluemix",
    }

    client = Cloudant.iam(
        account_name=secret["ACCOUNT_NAME"],
        api_key=secret["IAM_API_KEY"],
        url=secret["URL"],
        connect=True,
    )

    my_database = client["reviews"]
    print(my_database)

    try:
        selector = {'dealership': {'$eq': int(dict["dealerId"])}}
        result_by_filter = my_database.get_query_result(
            selector, raw_result=True)

        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': result_by_filter}

        }
        return result
    except:

        return {
            'statusCode': 404,
            'message': "Something went wrong"
        }