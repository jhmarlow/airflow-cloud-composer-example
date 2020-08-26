import pytest

def set_env(service_account_key):
     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
    
    
def test_env_set():
    service_account_key = 'test/path'
    
    set_env(service_account_key)
    
    assertisEqual(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'test/path')
    
    