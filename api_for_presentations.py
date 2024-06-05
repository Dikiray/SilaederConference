
from fastapi import FastAPI
from urllib.parse import urlparse
import re
import sqlite3
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
directions = 'математикабиологияфизикаробототехникаинформатикахимияанглийский языклитературалингвистикаистория'
def remake_data(projects, cur):
    result = projects
    for i in range(len(result)):
        que = "SELECT first_name, last_name FROM auth_user WHERE  id={}".format(result[i][4])
        cur.execute(que)
        teacher = cur.fetchall()
        result[i] = {'id': result[i][0], 'name': result[i][1], 'autors': result[i][3], 'time': result[i][6], 'presentation':{'pdf': 'http://api.conf.algo.silaeder.ru/' + result[i][2], 'videos': []}, 'teacher': teacher[0][1] + " " + teacher[0][0], 'direction': result[i][5]}
        que = "SELECT video_wishes, video FROM silsite_video WHERE project_id={}".format(result[i]['id'])
        cur.execute(que)
        videos = cur.fetchall()
        for j in videos:
            if 'v=' in j[1]:
                video = urlparse(j[1])[4].split('&')[0].replace('v=', '')
            else:
                video = j[1].split('/')[-1]
            if 'shorts' in j[1]:
                video = j[1].split('/')[-1]
            result[i]['presentation']['videos'].append({'after_slide': str(int(j[0]) + 1), 'YT': video})
    return result

@app.get("/projects")
def projects():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    que = "SELECT id, name, presentation,students, teacher_id, direction, time FROM silsite_project"
    cur.execute(que)
    result = cur.fetchall()
    result = remake_data(result, cur)
    cur.close()
    return result

@app.get("/project/{project_id}")
def project(project_id=None):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    que = "SELECT id, name, presentation, students, teacher_id, direction, time FROM silsite_project WHERE id={}".format(project_id)
    cur.execute(que)
    result = cur.fetchall()
    result = remake_data(result, cur)
    cur.close()
    return result[0]

@app.get("/project")
def project_by_name(q=None, t=None, s=None):
    global directions
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    que = "SELECT id, name, presentation, students, teacher_id, direction, time FROM silsite_project"
    cur.execute(que)
    result = cur.fetchall()
    result = remake_data(result, cur)
    cur.close()
    sorted_result = []
    if s:
        if len(re.findall(s, directions)) != 1:
            s = None
    for i in result:
       # print(i)
        if q:
           if q.lower() in i['name'].lower() or q.lower() in i['autors'].lower():
               sorted_result.append(i)
        if s and s in i['direction'].lower():
            sorted_result.append(i)
    return sorted_result
