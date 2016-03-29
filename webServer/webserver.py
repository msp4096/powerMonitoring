from wsgiref.simple_server import make_server

def application(environ, start_response):
    temp_1 = 99.6
    temp_2 = 12.3
    html_1 = '<html><header><title>Erics Pi</title></header><body>'
    html_2 = '<table border="1"><tr><td>Temp 1</td><td>'
    html_3 = '</td></tr><tr><td>Temp 2</td><td>'
    html_4 = '</td></tr></table</body></html>'
    # response_body = 'Hello Eric'
    response_body = html_1 + html_2 + str(temp_1) + html_3 + str(temp_2) + html_4
    status = '200 OK'

    # Some header magic, create response
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]





# Make it serve on all addresses
# can be changed to e.g. 192.168.0.10 of you want to restric to local network
httpd = make_server('0.0.0.0', 80, application)
httpd.serve_forever()
