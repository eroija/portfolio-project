from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from pprint import pprint
import os

app = Flask(__name__)
#app = Flask(__name__, template_folder='templates')

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'eric'
app.config['MYSQL_PASSWORD'] = 'kayamB4!'
app.config['MYSQL_DB'] = 'Drug_search'

mysql = MySQL(app)
print("ero")

@app.route("/", methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()

    # Execute the SQL query to search for the drug availability
    cur.execute("select drug_name from drugs")

    # Fetch the matching records
    results = cur.fetchall()
    results = [result[0] for result in results]
    return render_template('index.html', drugs = results)

@app.route("/chemist")
def chemist():
    return render_template('chemist.html')

@app.route("/drug")
def drug():

    return render_template('drug.html')

@app.route("/drug_search_helper")
def drug_search_helper():
    return render_template('drug_search_helper.html')

@app.route('/add_drug', methods=['GET', 'POST'])
def add_drug():
    if request.method == 'POST':
        # Get drug data from the form
        drug_name = request.form['drug_name']
        dosage_form = request.form['dosage_form']
        therapeutic_class = request.form['therapeutic_class']
        route_of_administration = request.form['route_of_administration']
        dosage_strength = request.form['dosage_strength']
        drug_id = request.form['drug_id']

        # Create a cursor object
        cur = mysql.connection.cursor()

        # Execute the SQL query
        cur.execute("INSERT INTO drugs(drug_name, dosage_form, therapeutic_class, route_of_administration, dosage_strength, drug_id) VALUES (%s, %s, %s, %s, %s, %s)", (drug_name, dosage_form, therapeutic_class, route_of_administration, dosage_strength, drug_id))

        # Commit to the database
        mysql.connection.commit()

        # Close the connection
        cur.close()

        # Return a success message
        return 'Drug added successfully!'
    else:
        # If it's not a POST request, you can display a form or a message
        return render_template('drug.html')

@app.route('/add_pharmacy', methods=['GET', 'POST'])
def add_pharmacy():
    if request.method == 'POST':
        # Get pharmacy data from the form
        pharmacy_name = request.form['pharmacy_name']
        location = request.form['location']
        drug_available = request.form['drug_available']
        address = request.form['address']
        operating_hours = request.form['operating_hours']
        contact_information = request.form['contact_information']
        wheelchair_accessible = request.form['wheelchair_accessible']

        # Create a cursor object
        cur = mysql.connection.cursor()

        # Execute the SQL query
        cur.execute("INSERT INTO pharmacy(pharmacy_name, location, drug_available, address, operating_hours, contact_information, wheelchair_accessible) VALUES (%s, %s, %s, %s, %s, %s, %s)", (pharmacy_name, location, drug_available, address, operating_hours, contact_information, wheelchair_accessible))

        # Commit to the database
        mysql.connection.commit()

        # Close the connection
        cur.close()

        return 'Pharmacy added successfully!'
    else:
        # Handle GET request, perhaps return a form for the user to fill out
        return render_template('chemist.html')
    
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get user data from the form
        user_name = request.form['user_name']
        name_of_drug = request.form['name_of_drug']
        name_of_pharmacy = request.form['name_of_pharmacy']

        # Create a cursor object
        cur = mysql.connection.cursor()

        # Execute the SQL query
        cur.execute("INSERT INTO users(user_name, name_of_drug, name_of_pharmacy) VALUES (%s, %s, %s)", (user_name, name_of_drug, name_of_pharmacy))

        # Commit to the database
        mysql.connection.commit()

        # Close the connection
        cur.close()

        return 'User added successfully!'
    else:
        # Handle GET request, perhaps return a form for the user to fill out
        return render_template('index.html')
    
@app.route('/submit-request', methods=['POST'])
def submit_request():
    # Get form data
    #user_name = request.form['userName']
    #import ipdb
    #ipdb.set_trace()
    drug_name = request.form['name_of_drug']
    pharmacy_name = request.form['name_of_pharmacy']
    user_location = request.form['userLocation']
    #request_id = request.form['requestId']
    print("drug_name: ", drug_name)
    print("pharmacy_name: ", pharmacy_name)
    print("user_location: ", user_location)

    # Create a cursor object
    cur = mysql.connection.cursor()

    # Execute the SQL query to search for the drug availability
    # cur.execute("SELECT * FROM drugs WHERE drug_name = %s", (drug_name,))
    cur.execute("""SELECT d.drug_id AS id, d.drug_name, d.dosage_form, d.therapeutic_class, d.route_of_administration, d.dosage_strength, pharmacy.pharmacy_name, pharmacy.contact_information 
FROM drugs AS d
INNER JOIN connect ON d.drug_id = connect.drug_id
INNER JOIN pharmacy ON connect.pharmacy_id = pharmacy.pharmacy_id
WHERE pharmacy.pharmacy_name = %s
  AND pharmacy.location = %s
  AND d.drug_name = %s""",
(pharmacy_name, user_location, drug_name));


#SELECT d.drug_id as id, d.drug_name, d.dosage_form, d.therapeutic_class, d.route_of_administration, d.dosage_strength, pharmacy.pharmacy_name
#FROM drugs as d
#INNER JOIN connect ON d.drug_id = connect.drug_id
#INNER JOIN pharmacy ON connect.pharmacy_id = pharmacy.pharmacy_id;


    # Fetch the matching records
    results = cur.fetchall()
   
    column_names = [col[0] for col in cur.description]

    results_list = []
    for row in results:
        row_map = {}
        for index, val in enumerate(row):
            row_map[column_names[index]] = val
        results_list.append(row_map)

    # Close the connection
    cur.close()

    # Check if we got any results
    if results:
        # Return the results as JSON
        pprint(jsonify(results_list))
        return jsonify(results_list)
    else:
        # Return a message if no data was found
        print( 'No matching records found')

    return {}

app.route("/first")
def home():
    return render_template('landingpage.html')

if __name__ == "__main__":
    app.run(debug=True)