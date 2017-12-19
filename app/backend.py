"""
    Backend for our ISTS website
    2/9/2017
    @author: Doshmajhan
"""

import code_generator
import flask
import MySQLdb
import random
import string
import time
from flask import Flask
from flask import jsonify
app = Flask(__name__)

resources = ['water', 'gas', 'food', 'electricity', 'luxury']


def connect_db():
    """
        Create our connection to the mysql database

        :return db: the object for our database connection
    """
    db = MySQLdb.connect(host='localhost', user='root', 
                         passwd='con162ess', db='ists')
    return db


def bad_auth():
    """
        Handles returning a not authenticated response

        :return response: the object containing our response text and status
    """
    resp = flask.Response('Authentication Failed', status=401, mimetype='text/html')
    return resp


def log_action(src, dst, action, data, ip):
    """
        Logs a action that is performed on the web app

        :param src: the cid of the country that performed the action
        :param dst: the cid of the country the action is performed against
        :param action: what was performed
        :param data: the information passed in the action
        :param ip: the ip of the source 
    """
    global db
    cur = db.cursor()
    t = time.time()
    cur.execute("INSERT INTO auditing (cidsrc, ciddst, action, data, time, ip) " \
                "VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (src, dst, action, data, t, ip))
    db.commit()


def authenticate(session):
    """
        Authenticates a country from the given session

        :param session: the session variable submitted in the request
        :returns status: status of the authentication, the cid if valid, None if invalid
    """
    global db
    cur = db.cursor()
    cur.execute("SELECT cid, time FROM sessions WHERE sessionid='%s'" % (session))
    result = cur.fetchone()
    if not result:
        return None
    
    cid = int(result[0])
    t = float(result[1])
    cur_time = time.time()
    diff_time = cur_time - t
    if diff_time > 36000:
        print "expired"
        return "expired"
    
    return cid


def check_ally(country1, country2):
    """
        Checks if two countries are allies when a new code for a resource
        is added, to determine if the resource is shared or stolen.

        :param country1: one of the country whose adding a resource, accept country or cid
        :param country2: the country the resource belongs to, accepts country or cid
        :return status: If the countries are allies or not, 1 if yes, 0 if no
    """
    global db
    cur  = db.cursor()

    if isinstance(country1, int):
        cid1 = country1
    else:
        cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country1))
        cid1 = cur.fetchone()
        cid1 = int(cid1[0])
    
    if isinstance(country2, int):
        cid2 = country2
    else:
        cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country2))
        cid2 = cur.fetchone()
        cid2 = int(cid2[0])

    cur.execute("SELECT atpeace%s FROM relations WHERE cid='%s'" % (cid1, cid2))
    check1 = cur.fetchone()
    cur.execute("SELECT atpeace%s FROM relations WHERE cid='%s'" % (cid2, cid1))
    check2 = cur.fetchone()

    if int(check1[0]) == 1 and int(check2[0]) == 1:
        return 1
    else:
        return 0


def check_resource(resource):
    """
        Checks which country the resource belongs to

        :param resource: the code for that specific resource
        :return country: the country the resource belongs to
        :return type: the type of resource the code is for
    """
    global db
    cur = db.cursor()

    for r in resources:
        cur.execute("SELECT cid FROM starting_resources WHERE has_%s='%s'" % (r, resource))
        cid = cur.fetchone()
        if cid:
            return (int(cid[0]), r)
    
    return (None, None)


def check_number_of_shares(cid, cid2):
    """
        Checks the number of resources shared from cid to cid2

        :param cid: the cid of the country sharing the resource
        :param cid2: the cid of the country getting the shared resource
        :return check: true if they haven't shared a resource yet, false if they have
    """
    global db
    cur = db.cursor()
    
    for r in resources:
        cur.execute("SELECT has_%s FROM starting_resources WHERE cid='%s'" % (r, cid))
        owned_resource = cur.fetchone()[0]
        if owned_resource == "0":
            continue
        
        cur.execute("SELECT has_%s FROM acquired_resources WHERE cid='%s'" % (r, cid2))
        shared_resource = cur.fetchone()[0]
        if shared_resource == "0":
            continue

        if owned_resource == shared_resource:
            return False

    return True


def resource_stolen(resource_type, code, cid, owner):
    """
        Handles when a resource is stolen from a country
        It will update the country who stole it with the code
        The country who was stolen from will lose it
        All the countries who shared it with the person who stole it will also lose it

        :param resource_type: the type of the resource being stolen
        :param code: the code for the stolen resource
        :param cid: the cid of the country stealing the resource
        :param owner: the owner of the resource being stolen

    """
    global db
    cur = db.cursor()
    cur.execute("UPDATE starting_resources SET has_%s='%s' WHERE cid='%s'" 
                % (resource_type, resource, cid))
    cur.execute("UPDATE starting_resources SET has_%s='0' WHERE cid='%s'"
                % (resource_type, resource_owner)) 

    country_list = [x for x in range(1, 11) if x != cid]
    for c in country_list:
        cur.execute("SELECT cid FROM acquired_resources WHERE has_%s='%s'" %
                    (resource_type, code))

        sharer = cur.fetchone()
        if not sharer:
            continue
        
        cur.execute("UPDATE acquired_resources SET has_%s='0' WHERE cid='%s'" %
                    (resource_type, c))

    db.commit()


def randomize_resource(resource, cid, old_code):
    """
        Re randomizes the resource of a given country after they have removed an ally
        so that there ally can't just take their code right after and re-enter it, also
        updates the code for the allies they share it with

        :param resource: the resource being randomized
        :param cid: the cid of the country
        :param old_code: the old code value
    """
    global db
    cur = db.cursor()
    new_code = code_generator.create_code()
    code_generator.update_code('starting_resources', new_code, resource, cid)
    cur.execute("SELECT cid FROM acquired_resources WHERE has_%s='%s'" % 
                (resource, old_code))
    ally_list = cur.fetchall()
    if ally_list:
        for ally in ally_list:
            cur.execute("UPDATE acquired_resources SET has_%s='%s' WHERE cid='%s'" %
                        (resource, new_code, ally[0]))



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Function to handle logging in of a certain country

        :param country: the country logging in
        :param password: the password for the country
        :return session: the newly created session token for that country
    """
    global db
    args = flask.request.args
    country = args['country']
    password = args['password']
    cur = db.cursor()
    cur.execute("SELECT cid FROM users WHERE countryname='%s' AND password='%s'" 
                % (country, password))

    cid = cur.fetchone()
    if not cid:
        return bad_auth()
    cid = int(cid[0])
    
    session = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
    t = time.time()
    ip = flask.request.remote_addr
    cur.execute("UPDATE sessions SET sessionid='%s', time='%s', ip='%s' WHERE cid=%s"
                % (session, t, ip, cid))
    db.commit()
    log_action(cid, 0, 'Logged in', 'none', flask.request.remote_addr)
    return session


@app.route("/authenticate", methods=['GET'])
def authenticate_endpoint():
    """
        Authenticates a country from the given session

        :param session: the session variable submitted in the request
        :returns status: status of the authentication, the cid if valid, None if invalid
    """
    global db
    args = flask.request.args
    session = args['session']
    if not session:
        status = {'False': 'No session'}
        return jsonify(status)

    cur = db.cursor()
    cur.execute("SELECT cid, time FROM sessions WHERE sessionid='%s'" % (session))
    result = cur.fetchone()
    if not result:
        return jsonify({'False': 'Bad session'})
    
    cid = int(result[0])
    t = float(result[1])
    cur_time = time.time()
    diff_time = cur_time - t
    if diff_time > 36000:
        return jsonify({'False': 'Session expired'})
    
    return str(cid)


@app.route('/getname', methods=['GET'])
def get_name():
    """
        Returns the name of the country that is logged in

        :param session: the session id of the country thats logged in
        :return name: the name of the country
    """
    global db
    args = flask.request.args
    session = args['session']
    cid = authenticate(session)
    if not cid:
        return bad_auth()
    elif cid == 'expired':
        status = {'False': 'Session expired'}
        return jsonify(status)

    cur = db.cursor()
    cur.execute("SELECT countryname FROM users WHERE cid='%s'" % (cid))
    name = cur.fetchone()
    if not name:
        status = {'False': 'Could not find your country, how are you even logged in'}
        return jsonify(status)

    status = {'True': '%s' % str(name[0]) }
    return jsonify(status)


@app.route('/getresources', methods=['GET'])
def get_resources():
    """
        Returns the resources currently owned by that country
        
        :param session: the session of the country requesting its resources
        :returns resource: a json object of the resources
    """
    global db
    args = flask.request.args
    session = args['session']
    cid = authenticate(session)
    if not cid:
        return bad_auth()
    elif cid == 'expired':
        status = {'False': 'Session expired'}
        return jsonify(status)

    cur = db.cursor()
    starting_resources = []
    acquired_resources = []
    json_data = {}

    for r in resources:
        cur.execute('SELECT has_%s FROM starting_resources WHERE cid=%s'
                    % (r, cid))
        code = cur.fetchone()
        if code[0] != "0":
            starting_resources += [(r, code[0])]
            continue

        cur.execute('SELECT has_%s FROM acquired_resources WHERE cid=%s'
                    % (r, cid))
        code = cur.fetchone()
        if code[0] != "0":
            acquired_resources += [(r, code[0])]

    json_data['starting_resources'] = starting_resources
    json_data['acquired_resources'] = acquired_resources
    return jsonify(json_data)


@app.route('/getallies', methods=['GET'])
def get_allies():
    """
        Returns the allies for the requesting country

        :param session: the session token for the requesting country
        :return allies_json: a json object of the allies 
    """
    global db
    args = flask.request.args
    session = args['session']
    country = args['country']  
    cur = db.cursor()
    if country: 
        cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country))
        cid = cur.fetchone()
        if not cid:
            status = {'False' : '%s is not a country' % country}
            return jsonify(status)
        cid = int(cid[0])

    else:
        cid = authenticate(session)
        if not cid:
            return bad_auth()
        elif cid == 'expired':
            status = {'False': 'Session expired'}
            return jsonify(status)

    allies_json = {}
    allies_json['allies'] = []
    
    for x in range(1, 11):
        cur.execute("SELECT atpeace%s FROM relations WHERE cid='%s'" % (x, cid))
        relation = cur.fetchone()
        relation = int(relation[0])
        if relation:
            cur.execute("SELECT countryname FROM users WHERE cid='%s'" % (x))
            country = cur.fetchone()[0]
            allies_json['allies'] += [country]

    return jsonify(allies_json)


@app.route('/getenemies', methods=['GET'])
def get_enemies():
    """
        Returns the enemies for the requesting country

        :param session: the session token for the requesting country
        :return enemies_json: a json object of the allies 
    """
    global db
    args = flask.request.args
    session = args['session']
    country = args['country']
    cur = db.cursor()
    if country:        
        cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country))
        cid = cur.fetchone()
        if not cid:
            status = {'False' : '%s is not a country' % country}
            return jsonify(status)
        cid = int(cid[0])

    else:
        cid = authenticate(session)
        if not cid:
            return bad_auth()
        elif cid == 'expired':
            status = {'False': 'Session expired'}
            return jsonify(status)

    enemies_json = {}
    enemies_json['enemies'] = []
    
    for x in range(1, 11):
        cur.execute("SELECT atwar%s FROM relations WHERE cid='%s'" % (x, cid))
        relation = cur.fetchone()
        relation = int(relation[0])
        if relation:
            cur.execute("SELECT countryname FROM users WHERE cid='%s'" % (x))
            country = cur.fetchone()[0]
            enemies_json['enemies'] += [country]

    return jsonify(enemies_json)


@app.route('/addally', methods=['GET', 'POST'])
def add_ally():
    """
        Handles request for adding an ally
    
        :param session: the session of the country adding an ally
        :param country: the name of the country being added
        :returns status: The status of the request, 200 for OK, 500+ if error
    """
    global db
    args = flask.request.args
    session = args['session']
    cid = authenticate(session)
    if not cid:
        return bad_auth()
    elif cid == 'expired':
        status = {'False': 'Session expired'}
        return jsonify(status)

    country_to_add = args['country']
    cur = db.cursor()

    cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country_to_add))
    cid2 = cur.fetchone()
    if not cid2:
        status = {'False': "%s isn't a country" % country_to_add}
        return jsonify(status)
    
    cid2 = int(cid2[0]) 
    if cid == cid2:
        status = {'False': "Can't add yourself" }
        return jsonify(status)
    
    count = 0
    for x in range(1, 12):
        cur.execute("SELECT atpeace%s FROM relations WHERE cid='%s'" % (x, cid))
        relation = cur.fetchone()
        relation = int(relation[0])
        if relation:
            count += 1
        if count >= 2:
            status = {'False': "Can't have more than 2 allies" }
            return jsonify(status)
    

    cur.execute("UPDATE relations SET atpeace%s='1' WHERE cid='%s'" % (cid2, cid)) 
    cur.execute("UPDATE relations SET atwar%s='0' WHERE cid='%s'" % (cid2, cid))
    
    db.commit()
    
    log_action(cid, cid2, 'Added ally', country_to_add, flask.request.remote_addr)
    status = {'True': '%s added as ally' % country_to_add}
    return jsonify(status)


@app.route('/makeneutral', methods=['GET', 'POST'])
def make_neutral():
    """
        Handles request for neutralizing a country
    
        :param session: the session of the country removing an ally
        :param country: the name of the country being removed
        :returns status: The status of the request, 200 for OK, 500+ if error
    """
    global db
    args = flask.request.args
    session = args['session']
    cid = authenticate(session)
    if not cid:
        return bad_auth()
    elif cid == 'expired':
        status = {'False': 'Session expired'}
        return jsonify(status)

    country_to_remove = args['country']
    cur = db.cursor()

    cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country_to_remove))
    cid2 = cur.fetchone()
    if not cid2:
        status = {'False': '%s is not a country' % country_to_remove}
        return jsonify(status)

    cid2 = int(cid2[0])
    if cid2 == cid:
        status = {'False': 'Can not remove yourself'}
        return jsonify(status)

    cur.execute("UPDATE relations SET atpeace%s='0' WHERE cid='%s'" % (cid2, cid))
    cur.execute("UPDATE relations SET atpeace%s='0' WHERE cid='%s'" % (cid, cid2))
    cur.execute("UPDATE relations SET atwar%s='0' WHERE cid='%s'" % (cid2, cid))
    cur.execute("UPDATE relations SET atwar%s='0' WHERE cid='%s'" % (cid, cid2))

    for r in resources:
        # Check if remover is using a resource of the removee, if so remove it
        cur.execute("SELECT has_%s FROM acquired_resources WHERE cid='%s'" % (r, cid))
        acquired_resource = cur.fetchone()
        acquired_resource = acquired_resource[0]
        cur.execute("SELECT has_%s FROM starting_resources WHERE cid='%s'" % (r, cid2))
        original_resource = cur.fetchone()
        original_resource = original_resource[0]
        if (acquired_resource == original_resource) and \
            (acquired_resource != "0" or original_resource != "0") :
            
            print "Removing %s from %d" % (r, cid)
            cur.execute("UPDATE acquired_resources SET has_%s='0' WHERE cid='%s'"
                        % (r, cid))

            #randomize_code(r, cid2, original_resource)

        # check if the removee is using a resource of the remover
        cur.execute("SELECT has_%s FROM starting_resources WHERE cid='%s'" % (r, cid))
        original_resource = cur.fetchone()
        original_resource = original_resource[0]
        cur.execute("SELECT has_%s FROM acquired_resources WHERE cid='%s'" % (r, cid2))
        acquired_resource = cur.fetchone()
        acquired_resource = acquired_resource[0]
        if (acquired_resource == original_resource) and \
            (acquired_resource != "0" or original_resource != "0"):
            
            print "Removing %s from %d" % (r, cid2)
            cur.execute("UPDATE acquired_resources SET has_%s='0' WHERE cid='%s'"
                        % (r, cid2))

            #randomize_code(r, cid, original_resource)

    db.commit()
    
    log_action(cid, cid2, 'Became neutral', country_to_remove, flask.request.remote_addr)
    status = {'True': '%s became neutral' % country_to_remove }
    return jsonify(status)


@app.route('/declarewar', methods=['GET', 'POST'])
def declare_war():
    """
        Handles request for declaring war on a team
        first for

        :param session: the session for the country declaring war
        :param country: the name of the country being declared against
        :returns status: The status of the request, 200 for OK, 500+ if error
    """
    global db
    args = flask.request.args
    session = args['session']
    cid = authenticate(session)
    if not cid:
        return bad_auth()
    elif cid == 'expired':
        status = {'False': 'Session expired'}
        return jsonify(status)

    country_to_attack = args['country']
    cur = db.cursor()

    cur.execute("SELECT cid FROM users WHERE countryname='%s'" % (country_to_attack))
    cid2 = cur.fetchone()
    if not cid2:
        status = {'False': '%s is not a country' % country_to_attack}
        return jsonify(status)

    cid2 = int(cid2[0])
    if cid2 == cid:
        status = {'False': 'Can not declare war against yourself'}
        return jsonify(status)

    cur.execute("UPDATE relations SET atwar%s='1' WHERE cid='%s'" % (cid2, cid))
    cur.execute("UPDATE relations SET atpeace%s='0' WHERE cid='%s'" % (cid2, cid))
    cur.execute("UPDATE relations SET atwar%s='1' WHERE cid='%s'" % (cid, cid2))
    cur.execute("UPDATE relations SET atpeace%s='0' WHERE cid='%s'" % (cid, cid2))

    db.commit()
    status = {'True' : 'Declared war against %s' % country_to_attack } 
    log_action(cid, cid2, 'declared war against', country_to_attack, flask.request.remote_addr)
    return jsonify(status)


@app.route('/addresource', methods=['GET', 'POST'])
def add_resource():
    """
        Handles adding a new resource to a country

        :param session: the session of the country adding a resource
        :param resource: the code of the resource being added
        :return status: status of the request, 200 for OK, 500+ for error
    """
    global db
    args = flask.request.args
    cur = db.cursor()
    session = args['session']
    country = args['country']
    cid = authenticate(session)
    if not cid:
        return bad_auth()
    elif cid == 'expired':
        status = {'False': 'Session expired'}
        return jsonify(status)

    resource = args['resource']
    resource_owner, resource_type = check_resource(resource)
    if not resource_owner or not resource_type:
        status = {'False': 'Bad resource code'}
        return jsonify(status)

    if country:
        cur.execute("SELECT cid FROM users WHERE countryname='%s'" % country)
        cid2 = cur.fetchone()
        if not cid2:
            status = {'False': '%s is not a country' % country}
            return jsonify(status)
            
        cid2 = int(cid2[0])
        if cid2 == cid:
            status = {'False': "Can't add your own resource"}
            return jsonify(status)

        if not check_number_of_shares(cid, cid2):
            status = {'False': "Can't share more than one resource with an ally"}
            log_action(cid, cid2, 'Tried to share more than one reource',
                        country + ',' + resource_type, flask.request.remote_addr)
            return jsonify(status)

        cur.execute("UPDATE acquired_resources SET has_%s='%s' WHERE cid='%s'"
                    % (resource_type, resource, cid2))
        db.commit()
        status = {'True': '%s shared with %s' % (resource_type, country)}
        log_action(cid, cid2, 'Shared resource with', country + ',' + resource_type, 
                    flask.request.remote_addr)

        return jsonify(status)

    if resource_owner == cid:
        status = {'False': "Can't add your own resource"}
        return jsonify(status)

    status = check_ally(cid, resource_owner)
    if status:
        cur.execute("UPDATE acquired_resources SET has_%s='%s' WHERE cid='%s'" 
                    % (resource_type, resource, cid))
        log_action(cid, cid2, 'Added resource', country + ',' + resource_type, 
                    flask.request.remote_addr)

    else:
        resource_stolen(resource_type, resource, cid, resource_owner) 
        log_action(cid, cid2, 'Stole resource', country + ',' + resource_type, 
                    flask.request.remote_addr)
    
    db.commit()       

    status = {'True': 'Resource added: %s' % resource}
    return jsonify(status)


db = connect_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
