import requests
import json
import  time
from datetime import  datetime,date,timedelta
import sys
from random import  randint
import  os


def RandomDate(startdate,enddate):
    delta=enddate-startdate
    return startdate+timedelta(days=randint(0,delta.days))


def main(stars):
    #
    # User Input
    #
    stars=str(stars)
    projList=[]
    username1 =input('Github username: ')
    username2 = input('Github username: ')
    username3 = input('Github username: ')
    password = input('Github pwd: ')
    cwd=os.getcwd()

    #
    # Compose Request
    #
    prjcnt=0
    fcsv=open(cwd+"/Experiments/SelectGithubRepos/ProjectURL.csv",'a')

    i=0

    smallerdate=date(2018,7,1)
    largerdate=date(2018,8,8)


    numofdays=(largerdate-smallerdate).days
    for i in range(0,numofdays):
    #for i in range(0,3200):

        #smallerdate=date(2008,01,12)+timedelta(days=i)
        #largerdate=date(2008,01,12)+timedelta(days=i+1)


        largerdate=date(2018,8,8) - timedelta(days=i)
        smallerdate=date(2018,8,8) - timedelta(days=i+1)

        if(smallerdate<date(2008,1,12)):
            break

        starsmall=stars
        print('smaller star is '+str(starsmall))
        print('smaller date is '+str(smallerdate))
        print('larger date is '+str(largerdate))


        rangeLimiter=10
        for p in range(1,11):
            try:
                if(p>rangeLimiter):
                    break

                if(p%2==0):
                    username=username1
                elif(p%3==0):
                    username=username2
                else:
                    username=username3
                url="https://api.github.com/search/repositories?q=stars:%3E="+str(stars)+ " created:"+str(smallerdate)+".."+str(largerdate)+"&per_page=100&page="+str(p)
                #url="https://api.github.com/search/repositories?q=stars:%3E="+str(s1)+"&page="+str(r)+"&created:"+str(smallerdate)+"..."+str(largerdate)+"&per_page=100"


                #url="https://api.github.com/search/repositories?q=stars:"+str(starsmall)+".."+str(starlarge)+"&page="+str(r)+"&created:"+str(smallerdate)+"..."+str(largerdate)+"&per_page=100"
                #url="https://api.github.com/search/repositories?q=stars:"+str(1)+".."+str(j+2000000)+"&page="+str(i)+"&per_page=100"


                urlrate='https://api.github.com/rate_limit'
                f=open(cwd+"/Experiments/SelectGithubRepos/"+stars+"_"+str(p)+'_'+str(smallerdate)+'_'+str(largerdate)+".json",'w')


                payload = {}
                res = requests.get(
                    url,
                    auth = (username, password),
                    data = json.dumps(payload),
                    )


                data=json.loads(res.text)
                try:
                    rangeLimiter=(data['total_count']//1000)+1
                except:
                    ferr=open(cwd+"/Experiments/SelectGithubRepos/"+stars+"_err"+".txt",'w')
                    ferr.write(str(smallerdate)+"::"+str(largerdate)+"\n")
                    ferr.close()
                    break


                if(rangeLimiter>10):
                    print("ERROR")
                    ferr=open(cwd+"/Experiments/SelectGithubRepos/"+stars+"_err"+".txt",'w')
                    ferr.write(str(smallerdate)+"::"+str(largerdate)+"\n")
                    ferr.close()
                    break
                json.dump(data, f)
                #f.write(res.text)
                f.close()
                #print res.text
                try:
                    for k in data['items']:
                        if(k['html_url'] not in projList):
                            projList.append(k['html_url'])
                            print("Project Number "+str(prjcnt)+": "+k['html_url'])
                            fcsv.write(str(prjcnt)+","+k['html_url']+","+str(k['stargazers_count'])+"\n")
                            prjcnt+=1
                        else:
                            print("ERROR DUP FOUND")
                except:
                    print(sys.exc_info())
                    print("ERROR")
                    print(data)
                    ferr=open(cwd+"/Experiments/SelectGithubRepos/"+stars+"_"+str(i)+"_err_"+".txt",'w')
                    ferr.write(str(smallerdate)+"::"+str(largerdate)+"\n")
                    ferr.close()




                res2 = requests.get(
                    urlrate,
                    auth = (username, password),
                    data = json.dumps(payload),
                    )

                resetime=json.loads(res2.text)['resources']['search']['reset']


                print ("Start : %s" % time.ctime())
                print(data['total_count'])
                print("Time at which rate resets for username "+username+" is ::" +str(datetime.fromtimestamp(resetime).strftime('%c')))
                #check=(prjcnt)%1020
                #print(data)
                print("projcount :"+ str(prjcnt))
                #print("check :"+ str(check))
                if(1==2):
                    time.sleep(60)
                else:
                    time.sleep(4)

                print( "End : %s" % time.ctime())
            except:
                ferr=open(cwd+"/Experiments/SelectGithubRepos/"+stars+"_err"+".txt",'w')
                ferr.write(str(smallerdate)+"::"+str(largerdate)+"\n")
                ferr.close()

        #i+=1
    fcsv.close()


if __name__ == '__main__':
    stars=1000
    main(stars)
