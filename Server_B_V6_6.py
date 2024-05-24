import http.server
import json
import logging

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("Received POST request: %s", post_data.decode('utf-8'))

        try:
            data = json.loads(post_data)
            response = self.handle_request(data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Invalid JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_request(self, data):
        if "AlarmInfoPlate" in data:
            # Return the new response content based on the protocol document
            logging.info("receive info")
            response = {
		    "Response_AlarmInfoPlate": {
			    "info": "ok",
			    "content": "retransfer_stop",
			    "is_pay": "true",
			    "serialData": []
		    }
	    }
        else:
            # Existing functionality
            response = {"status": "received"}
        
        return response

def run(server_class=http.server.HTTPServer, handler_class=MyHandler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd on port %d...", port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
