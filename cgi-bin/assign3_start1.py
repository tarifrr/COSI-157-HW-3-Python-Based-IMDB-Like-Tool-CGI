#!/usr/bin/env python
import MySQLdb
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import os
import urllib

def query2():
    field=cgi.FieldStorage()
    form=field.getvalue('submit','null')
    category=field.getvalue('category','null')
    query=None

    string=form.split()
    string_set=''

    for i in string:
        string_set=string_set+"'%s' "%(i)

    form=','.join(string_set.split())

    

    if category=="movie":
        query="""select distinct movie_id,title,year_release,description,photo,trailer_link from movie where title in (%s) and is_rented='0'"""%form
    elif category=="actor":
        query="""select distinct movie.movie_id,title,year_release,description,photo,trailer_link from cast,castmovie,movie where movie.movie_id=castmovie.movie_id and castmovie.cast_id=cast.cast_id and (cast.first_name in (%s) or cast.last_name in (%s)) and is_rented='0'"""%(form,form)
    elif category=="director":
        query="""select distinct movie.movie_id,title,year_release,description,photo,trailer_link from director,castmovie,movie where movie.movie_id=castmovie.movie_id and castmovie.director_id=director.director_id and (director.first_name in (%s) or director.last_name in (%s)) and is_rented='0'"""%(form,form)
    
    if query!=None:
        
        db = MySQLdb.connect("localhost","root","pass1","assign3")
        c = db.cursor()
        c.execute(query)
        data=c.fetchall()

        i=0


        if len(data)==0:
            print "NO RESULTS HAVE BEEN FOUND"


        else:
            print """<form><div class="expandable">"""

            print """<table id='table' border="1">
            <tr><th>Movie ID</th><th>Title</th><th>Date of Release</th><th onclick="testing(this)">Click Here to Expand/Contract Description</th>
            <th>Photo</th><th>View Trailer</th><th>RENT ME</th></tr>"""

            while i<len(data):

                #urllib.urlopen('http://localhost//videostore//htdocs//img//temp.jpg',data[i][3]).

                path=os.path.abspath('.'+os.curdir)+"\\htdocs\\img\\%s.jpg"%data[i][0]

                fil=open(path,'wb')

                fil.write(data[i][4])

                fil.close()

               
                
                print """
                
                <tr><td>%s</td><td>%s</td><td>%s</td>
                <td><p>%s</p></td>
                <td><img src="/htdocs/img/%s.jpg" width=100 height=100></td>
                <td><a href="%s">Click To View Trailer</a></td>
                <td><input name="%s" id="%s" type="checkbox"> </td>    
                   

                </tr>"""%(data[i][0],data[i][1],data[i][2],data[i][3],data[i][1],data[i][5],i,i)

                i=i+1
                
            print """</table>"""


           


            print """
                    </div>
                    <br/><br/>
                    
                    <input type="button" id="xaction" value='Check Out' onclick="loadXMLDoc(this)">

                </form> 
                """    
            
            
            db.close()

def basic():

    print """Content-Type: text/html """

    print

    

    query2()


    

basic()






