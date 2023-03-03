def check_tokens_list(chromex):
    # Check if the tokens list is loaded
    result = chromex.Runtime.evaluate(expression="document.getElementById('tokens-list').innerHTML")
    try : 
        result = result[1][0]['result']['result']['value']
    except:
        return False
    else:
        return True
    