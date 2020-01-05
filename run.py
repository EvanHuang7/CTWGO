# when you import package, it will import __init__.py automatically
from ctwgo import create_app

app = create_app()

# this condition is true, when we run this scripte directly
if __name__ == '__main__':
	app.run(debug=True)