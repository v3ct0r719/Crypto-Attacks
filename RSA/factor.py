import requests

def factordb(p):
    try:
        a=requests.get("http://factordb.com/api", params={"query": str(p)}).json()
        fac = a['factors']
        for i in range(len(fac)):
            fac[i][0]=int(fac[i][0])
        return fac
    except:
        print "No Internet Connection"

