from flask import Flask, request # type: ignore

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def receive_data(path):
    # Save each export to a different file based on the path
    filename = f"jsonfiles/madden_export_{path.replace('/', '_') or 'root'}.json"
    data = request.get_data()
    with open(filename, 'wb') as f:
        f.write(data)
    return 'Data received!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)