from flask import Flask, jsonify, request
import os
import whois

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"success": true})

@app.route('/check_domain', methods=['GET'])
def check_domain():
    domain = request.args.get('domain', '')

    try:
        w = whois.whois(domain)
        if w.status == None:
            result = {"available": True}
        else:
            result = {
                "available": False,
                "status": w.status,
                "registered_on": w.creation_date,
                "expires_on": w.expiration_date,
                "updated_on": w.updated_date,
                "registrar": w.registrar
            }
    except Exception as e:
        result = {"available": True,"error": str(e)}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
