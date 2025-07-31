from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def test_page():
    return render_template('test.html', title="Test Page", content="This is a test")

if __name__ == '__main__':
    app.run(debug=True)