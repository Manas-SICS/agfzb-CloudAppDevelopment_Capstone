# IBM Cloud-specific imports
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
    
    db = client["reviews"]
    new_review = db.create_document(dict["review"])   
    
    if new_review.exists():
        result = {
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Review posted successfully."}
        }
    
        print(new_review)
        return result
        
    else: 
        error_json = {
            "statusCode": 500,
            "message": "Could not post review due to server error."
        }
        return error_json