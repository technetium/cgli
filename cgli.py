import argparse
import cgi
import json
import os
import sys
from urllib.parse import parse_qs

def show_form(arguments):
    print ("Content-Type: text/html; charset=utf-8")
    print ('')
    print('<!DocType html>')
    print('<html>')
    print('<head>')
    print('<meta charset="utf-8"/>')
    print('</head>')
    print('<body>')
    print('<form action="%s" method="post">' % os.environ.get('SCRIPT_NAME') )
    print('<table>')
    for key, value in arguments.items():
        print ('<tr>')
        print('<td>%s</td>' % key)
        print('<td><input name="%s" /></td>' % key)
    print ('<tr><td></td><td><input type="submit"></td></tr>')
    print ('</table>')
    print('</form>')
    print('</body>')
    print('</html>')
    exit()

def parse_arguments_cgi(arguments):
    if "h" == os.environ.get('QUERY_STRING'):
        show_form(arguments)

    if "POST" == os.environ.get('REQUEST_METHOD'):
        #print("Content-type: 'application/json; charset=utf-8")
        pass
    else:
        #print ("Content-Type: text/html")
        pass
    #print ('')
    args = {}
    form = cgi.FieldStorage()
    for key, value in arguments.items():
        args[key] = form.getfirst(key)
        if None == args[key]:
            if None != value.get('default'):
                args[key] = value['default']
        elif value.get('type'): 
            args[key] = (value['type'])(args[key])
    return args

def parse_arguments_cli(arguments):
    parser = argparse.ArgumentParser()
    for key, value in arguments.items():
        keys = ['--' + key]
        if 'short' in value:
            keys.append('-' + value['short'])
            del value['short']
        parser.add_argument(*keys, **value)
    args = {}
    for key, value in vars(parser.parse_args()).items():
        if (None != value):
            args[key] = value
    return args

def parse_arguments_wsgi(arguments, environ):
    form = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
    if (('CONTENT_LENGTH' in environ) and environ['CONTENT_LENGTH']):
        size = int(environ['CONTENT_LENGTH'])
        body = environ['wsgi.input'].read(size)
        form = parse_qs(body.decode('UTF-8'), keep_blank_values=True)
    
    args = {}
    for key, value in arguments.items():
        args[key] = form[key] if key in form else None
        if None == args[key]:
            if None != value.get('default'):
                args[key] = value['default']
        elif value.get('type'): 
            args[key] = (value['type'])(args[key])
    return args

def print_headers(status, headers):
    for (key, value) in headers:
        print('%s: %s' % (key, value)) 
    print('')
        
def do_nothing(status, headers):
    pass
    
def application_maker(method, arguments):

    def application(environ, start_response):
        cli = environ.get('command_line')
        #cli = None
        if None == cli:
            args = parse_arguments_wsgi(arguments, environ)
        elif cli:
            args = parse_arguments_cli(arguments)      
        else:
            args = parse_arguments_cgi(arguments)
        
        #result = environ
        #content = json.dumps(result)
        status = '200 OK'

        result = method(**args)
        if isinstance(result, dict):
            headers = [
                ('Content-type', 'application/json; charset=utf-8'),
                ('Access-Control-Allow-Origin', 'null'), 
            ]
            content = json.dumps(result, indent=4, sort_keys=True)
        else: 
            headers = [
                ('Content-Type', 'text/html; charset=utf-8')
            ]
            content = result
    
        start_response(status, headers)
        return [ str(content) ]
    
    return application

def application_execute(application):
    if None == os.environ.get('UWSGI_ORIGINAL_PROC_NAME'):
        ## We are not in the wsgi environment, we have to print something
        env = dict(os.environ)
        env['command_line'] = not ('QUERY_STRING' in os.environ)
        if env['command_line']:
            print_funct = do_nothing
        else:
            print_funct = print_headers
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)    
        print(''.join(application(env, print_funct)))
