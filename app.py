import backend.final as sync_gdata
from flask import Flask,request,send_from_directory,send_file

app=Flask(__name__,static_folder="./frontend/assets",template_folder="./frontend")


@app.route("/")
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory(app.static_folder, path)

@app.route('/download',methods=['GET'])
def download():
    query=request.args.get('query')
    excel_buffer=sync_gdata.search(query)
    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name=f"{query}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
 

if __name__ == '__main__':
    app.run(debug=True)