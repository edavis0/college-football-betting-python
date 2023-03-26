import cfbd
from dotenv import load_dotenv
import os

# Configure API key authorization and create an instance of the API class
def GetAPIInstance():
    configuration = cfbd.Configuration()
    load_dotenv()
    token = os.environ.get("api-token")
    configuration.api_key['Authorization'] = token
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    betting_api_instance = cfbd.BettingApi(cfbd.ApiClient(configuration))
    
    return(betting_api_instance)

